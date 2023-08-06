import os
import time
from email.generator import Generator
from json import JSONDecodeError
from typing import List

import requests
from sarina.core.logging import console
from sarina.core.task import BaseError
from sarina.core.utils import PromptField, dataclass

from .base import CDNProvider, Domain, ProviderError, ProvisioningError, Server


class APIError(BaseError):
    pass


class ArvanAPI:
    api_url: str = "https://napi.arvancloud.com/cdn/4.0/"

    def __init__(self, key):
        self.api_key = key

    def request(self, method, url_parts, *args, **kwargs):
        url_parts = [u.strip("/") for u in url_parts]
        url = os.path.join(self.api_url, *url_parts)
        resp = requests.request(
            method,
            url,
            headers={
                "Authorization": f"ApiKey {self.api_key}",
                "Accept": "application/json",
            },
            # proxies={"https": "http://localhost:8080"},
            # verify=False,
            # allow_redirects=False,
            *args,
            **kwargs,
        )
        return self.handle_data_response(resp)

    def get(self, *args):
        return self.request("GET", args)

    def delete(self, *args):
        return self.request("DELETE", args)

    def post(self, *args, json=None):
        return self.request("POST", args, json=json)

    def put(self, *args, json=None):
        return self.request("PUT", args, json=json)

    def patch(self, *args, json=None):
        return self.request("PATCH", args, json=json)

    def handle_data_response(self, resp: requests.Response):
        try:
            if resp.status_code == 404:
                return None
            if 200 <= resp.status_code < 300:
                return resp.json().get("data")
            if 300 <= resp.status_code < 400:
                raise APIError(
                    f"Recieved redirect response for '{resp.headers['Location']}'"
                )
            raise APIError(f"{resp.status_code}: {resp.json()['message']}")
        except JSONDecodeError:
            raise APIError(f"{resp.status_code}: {resp.text}")


@dataclass
class ArvanDomain(Domain):
    def update_dns_with_servers(
        self, servers: List[Server], cloud_proxy=True
    ) -> Generator:
        yield f"Fetching domain {self.sld}"

        api_domain = self.api.get("domains", self.sld)
        if api_domain is None:
            raise ProviderError(f"Domain {self.sld} does not exist in Arvan account")

        if api_domain.get("status", "") != "active":
            console.warn(f"Domain {self.sld} is not active")

        dns_update = {
            "type": "a",
            "name": self.dns_name,
            "value": [
                {"ip": s.ip, "port": None, "weight": 1, "country": ""} for s in servers
            ],
            "ttl": 120,
            "cloud": cloud_proxy,
            "upstream_https": "default",
            "ip_filter_mode": {"count": "multi", "order": "rr", "geo_filter": "none"},
        }

        yield f"Fetching DNS records for {self.sld}"
        dns_records = self.api.get("domains", self.sld, "dns-records")

        for record in dns_records:
            if record.get("type") == "a" and record.get("name") == self.dns_name:
                # Arvan errors on duplicates, so only send update if something changed
                needs_update = False
                dns_update["value"].sort(key=lambda v: v["ip"])
                record.get("value", []).sort(key=lambda v: v["ip"])
                for f in dns_update:
                    if record.get(f) != dns_update[f]:
                        needs_update = True
                        break
                if needs_update:
                    if len(servers) == 0:
                        yield f"Removing DNS record '{self.dns_name}'"
                        self.api.delete(
                            "domains", self.sld, "dns-records", record.get("id")
                        )
                    else:
                        yield f"Updating DNS record '{self.dns_name}' with {len(servers)} IPs"
                        self.api.put(
                            "domains",
                            self.sld,
                            "dns-records",
                            record.get("id"),
                            json=dns_update,
                        )
                else:
                    yield f"DNS Record '{self.dns_name}' is up to date"
                break
        else:
            if len(servers) > 0:
                yield f"Creating DNS record '{self.dns_name}' with {len(servers)} IPs"
                self.api.post("domains", self.sld, "dns-records", json=dns_update)
            else:
                yield f"DNS record for '{self.dns_name}' already removed"

    def provision(self) -> Generator:
        data = self.api.get("domains", self.sld)

        if not data["status"] == "active":
            for i in range(361):
                yield f"Waiting for ns records to get updated [{i}/360s]"
                # Check every 30 seconds
                if i % 30 == 0:
                    resp = self.api.get("/domains", self.sld, "ns-keys/check")
                    if resp["ns_status"] is True:
                        break
                if i == 0:
                    console.log(
                        "Please set these records as the [bold]authorative nameservers[/bold] for the domain"
                    )
                    for ns in data["ns_keys"]:
                        console.log(ns, style="orange1")
                time.sleep(1)
            else:
                raise ProvisioningError("Timed out waiting for ns records to update")

        yield "Fetching SSL status"
        ssl = self.api.get("/domains", self.sld, "ssl")

        if not ssl["certificates"]:
            # SSL certificate creation doesn't work when DNS records don't exist
            # So we make sure something exists before asking for a certificate
            yield "Checking DNS record exists"
            records = self.api.get("/domains", self.sld, "dns-records")
            for r in records:
                if r["type"] == "a" and r["name"] == self.dns_name:
                    break
            else:
                yield "Creating dummy DNS record"
                self.api.post(
                    "domains",
                    self.sld,
                    "dns-records",
                    json={
                        "type": "a",
                        "name": self.dns_name,
                        "value": [
                            {"ip": "1.2.3.4", "port": None, "weight": 1, "country": ""}
                        ],
                        "ttl": 120,
                        "cloud": True,
                        "upstream_https": "default",
                        "ip_filter_mode": {
                            "count": "multi",
                            "order": "rr",
                            "geo_filter": "none",
                        },
                    },
                )

            yield "Requesting certificate creation"
            self.api.patch(
                "/domains",
                self.sld,
                "ssl",
                json={
                    "certificate": "managed",
                },
            )

            yield "Waiting for certificates to be created"
            for i in range(1801):
                if i % 60 == 0:
                    ssl = self.api.get("/domains", self.sld, "ssl")
                    if ssl["certificates"]:
                        return True
                yield f"Waiting for certificates to be created [{i}/1800s]"
                time.sleep(1)

            raise ProvisioningError("Certificate creation timed out")

        yield "Activating SSL"
        if not ssl["ssl_status"]:
            self.api.patch(
                "/domains",
                self.sld,
                "ssl",
                json={
                    "ssl_status": True,
                },
            )

    @property
    def api(self):
        return self.provider.api


@dataclass
class ArvanProvider(CDNProvider):
    cloud = "ArvanCloud"
    domain_cls = ArvanDomain

    api_key: str = PromptField()

    _api = None

    def create_domain(self, domain_name: str) -> Generator:
        domain = ArvanDomain(name=domain_name, provider=self)

        yield "Checking domain status"

        api_domain = self.api.get("domains", domain.sld)
        if api_domain is None:
            yield f"Registering new domain {domain.sld} with Arvan"
            api_domain = self.api.post(
                "/domains/dns-service",
                json={"domain": domain.sld, "domain_type": "full", "plan_level": 1},
            )
        return domain

    @property
    def api(self):
        if self._api is None:
            self._api = ArvanAPI(self.api_key)
        return self._api
