import dataclasses
import os
import shutil
import traceback
from copy import deepcopy
from datetime import datetime
from typing import List, Optional

import yaml
from sarina.core.logging import console
from sarina.core.task import BaseError
from sarina.core.utils import dataclass
from sarina.monitoring.monitoring import Monitoring
from sarina.providers.base import Domain, Provider, Server
from sarina.templates.base import Template

DEFAULT_CONFIG_DIR = os.path.expanduser("~/.sarina")


@dataclass
class Cluster:
    name: str
    servers: List[Server]
    domains: List[Domain]
    template: Template

    def get_server(self, name=None, id=None) -> Server:
        if name is None and id is None:
            raise ValueError("Must specify either name or id")

        for s in self.servers:
            if (name is None or s.name == name) and (id is None or s.id == id):
                return s
        return None

    def get_domain(self, name) -> Domain:
        for d in self.domains:
            if d.name == name:
                return d
        return None

    @classmethod
    def new(cls, name):
        return cls(
            name=name,
            servers=[],
            domains=[],
            template=None,
        )


@dataclass
class Config:
    providers: List[Provider]
    clusters: List[Cluster]
    current_cluster: Cluster
    monitoring: Monitoring

    provider_cls = []
    template_cls = []

    def get_provider(self, name) -> Provider:
        for p in self.providers:
            if p.name == name:
                return p
        return None

    def get_cluster(self, name) -> Cluster:
        for c in self.clusters:
            if c.name == name:
                return c
        return None

    def get_all_servers(self) -> List[Server]:
        servers = []
        for c in self.clusters:
            servers.extend(c.servers)
        return servers

    def get_all_domains(self) -> List[Domain]:
        domains = []
        for c in self.clusters:
            domains.extend(c.domains)
        return domains

    @property
    def server_providers(self):
        return [p for p in self.providers if p.can_server]

    @property
    def cdn_providers(self):
        return [p for p in self.providers if p.can_cdn]

    def asdict(self):
        return dataclasses.asdict(self, dict_factory=self.dict_factory)

    def asjson(self, *args, **kwargs):
        import json

        return json.dumps(self.asdict(), *args, **kwargs)

    def asyaml(self, *args, **kwargs):
        import yaml

        return yaml.safe_dump(self.asdict(), *args, **kwargs)

    def dict_factory(self, args):
        def clean(k, v):
            if k.startswith("_"):
                return None
            if k == "provider":
                return k, v["name"]
            if k == "current_cluster":
                return "default_cluster", v["name"] if v else ""
            return k, v

        args = [clean(*a) for a in args]
        return dict([a for a in args if a is not None])

    def save(self, path):
        # Backup existing config incase we mess things up when saving new one
        backup_dir = os.path.join(DEFAULT_CONFIG_DIR, "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        if os.path.exists(path):
            bkup = os.path.join(
                backup_dir, f"config-{datetime.now().strftime('%Y%m%d-%H%M%S')}.yaml"
            )
            shutil.copyfile(path, bkup)

        try:
            data = self.asyaml(sort_keys=False)
        except Exception as e:
            console.error(traceback.format_exc())
            console.error("Saving config failed")
            return

        with open(path, "w") as f:
            f.write(data)


class ConfigError(BaseError):
    pass


def load_config(path, use_cluster=None, provider_cls=[], template_cls=[]):
    config = Config(providers=[], clusters=[], current_cluster=None, monitoring=None)
    config.provider_cls = provider_cls
    config.template_cls = template_cls

    if os.path.exists(path):
        with open(path) as f:
            data = yaml.safe_load(f.read())
    else:
        console.log(f"Starting fresh config at {path}")
        data = {}

    original_data = deepcopy(data)

    config.providers = parse_providers(provider_cls, data.get("providers", []))
    config.clusters = parse_clusters(config, template_cls, data.get("clusters", []))

    if use_cluster is None:
        use_cluster = data.get("default_cluster") or None
    if use_cluster is not None and config.get_cluster(use_cluster) is None:
        raise ConfigError(f"Cluster '{use_cluster}' does not exist")
    config.current_cluster = config.get_cluster(use_cluster)

    config.monitoring = parse_monitoring(config, data.get("monitoring"))

    # if config.asdict() != original_data:
    #     diff = DeepDiff(original_data, config.asdict())
    #     print(config.asdict())
    #     print(diff.pretty())
    #     raise ConfigError("Config dump mismatch")

    return config


def parse_providers(provider_cls, data):
    providers = []
    for p in data:
        for cls in provider_cls:
            if p.get("cloud") == cls.cloud:
                providers.append(cls(**p))
                break
        else:
            console.warn(
                f"Provider '{p.get('name')}' has an unknown cloud '{p.get('cloud')}', skipping provider."
            )
    return providers


def parse_clusters(config: Config, template_cls, data):
    clusters = []
    for c in data:
        try:
            clusters.append(parse_cluster(config, template_cls, c))
        except ConfigError as e:
            console.warn(
                f"Unable to parse cluster '{c.get('name')}': {str(e)}. Skipping cluster"
            )
    return clusters


def parse_cluster(config: Config, template_cls, data):
    if not data.get("name"):
        raise ConfigError("Missing name")

    cluster = Cluster.new(data.get("name"))

    for s in data.get("servers", []):
        try:
            cluster.servers.append(parse_server(config, s))
        except ConfigError as e:
            console.warn(
                f"Unable to parse server '{s.get('name')}': {str(e)}. Skipping server"
            )

    for d in data.get("domains", []):
        try:
            cluster.domains.append(parse_domain(config, d))
        except ConfigError as e:
            console.warn(
                f"Unable to parse domain '{d.get('name')}': {str(e)}. Skipping domain"
            )

    cluster.template = parse_template(template_cls, data.get("template", {}))

    return cluster


def parse_server(config: Config, data):
    name = data.get("name")
    if not name:
        raise ConfigError("Missing name")

    if not data.get("ip"):
        raise ConfigError("Missing ip")

    provider = config.get_provider(data.get("provider"))
    if provider is None:
        raise ConfigError(f"Unknown provider '{data.get('provider')}'")

    if not provider.can_server:
        raise ConfigError(
            f"Referring to provider '{data.get('provider')}' which does not support servers"
        )

    data["provider"] = provider
    return provider.server_cls(**data)


def parse_domain(config: Config, data):
    name = data.get("name")
    if not name:
        raise ConfigError("Missing name")

    provider = config.get_provider(data.get("provider"))
    if provider is None:
        raise ConfigError(f"Unknown provider '{data.get('provider')}'")

    if not provider.can_cdn:
        raise ConfigError(
            f"Referring to provider '{data.get('provider')}' which does not support domains"
        )

    data["provider"] = provider
    return provider.domain_cls(**data)


def parse_template(template_cls, data) -> Optional[Template]:
    if not data:
        raise ConfigError("Missing template")

    for cls in template_cls:
        if data.get("type") == cls.type:
            return cls(**data)
    else:
        raise ConfigError(f"Template has an unknown type '{data.get('type')}'")
    return None


def parse_monitoring(config: Config, data: dict) -> Optional[Monitoring]:
    if not data:
        return None

    server_data = data.get("server", None)
    server = None
    if server_data:
        try:
            server = parse_server(config, server_data)
        except ConfigError as e:
            console.warn(f"Unable to parse monitoring server config: {str(e)}")
            return None

    domain_data = data.get("domain", None)
    domain = None
    if domain_data:
        try:
            domain = parse_domain(config, domain_data)
        except ConfigError as e:
            console.warn(f"Unable to parse monitoring data config: {str(e)}")
            return None

    return Monitoring(server=server, domain=domain)
