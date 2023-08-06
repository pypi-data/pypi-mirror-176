import os
import time
from typing import Generator, List

import paramiko
import tld
from sarina.core.logging import console
from sarina.core.task import BaseError
from sarina.core.utils import PromptField, dataclass


class ProviderError(BaseError):
    pass


class ProvisioningError(BaseError):
    pass


@dataclass
class Provider:
    domain_cls = None
    server_cls = None

    cloud: str
    name: str

    @property
    def can_server(self):
        return self.server_cls is not None

    @property
    def can_cdn(self):
        return self.domain_cls is not None

    def init_provider(self):
        yield "Provider ready"


@dataclass
class ServerProvider(Provider):
    ssh_key: str = PromptField(default="~/.ssh/id_rsa", type="filepath")
    ssh_user: str = PromptField(default="root")

    def create_server(self, name) -> "Server":
        raise NotImplemented()

    def fetch_cluster_servers(self, cluster) -> List["Server"]:
        raise NotImplemented()

    def fetch_server(self, id) -> "Server":
        raise NotImplemented()

    @property
    def ssh_key_path(self):
        return os.path.expanduser(self.ssh_key)


@dataclass
class CDNProvider(Provider):
    def create_domain(self, domain_name: str) -> Generator:
        raise NotImplemented()


@dataclass
class Server:
    name: str
    ip: str
    provider: Provider
    id: str

    _client: paramiko.SSHClient = None

    @property
    def pname(self) -> str:
        return f"{self.provider.name}/{self.name}"

    @property
    def is_connected(self):
        return self._client is not None

    def connect(self, retries=8, retry_backoff=4) -> Generator:
        for r in range(retries):
            yield f"attempt [{r+1}/{retries}]"
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            user = self.provider.ssh_user or "root"
            try:
                client.connect(
                    self.ip,
                    port=22,
                    username=user,
                    key_filename=self.provider.ssh_key_path,
                )
                self._client = client
                return
            except Exception as e:
                if r == retries - 1:
                    self._client = None
                    raise
                time.sleep(retry_backoff)

    def run(self, *cmd) -> Generator:
        if self._client is None:
            raise ProviderError("Client not connected")

        tran = self._client.get_transport()
        chan = tran.open_session()
        chan.get_pty()
        f = chan.makefile()
        chan.exec_command(" ".join(cmd))

        lines = []
        max_line_len = 80
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            lines.append(line)
            if len(line) > max_line_len:
                yield line[:max_line_len] + "..."
            else:
                yield line

        if chan.recv_exit_status() != 0:
            console.error(lines[-15:])
            raise ProvisioningError()

    def destroy(self) -> Generator:
        raise NotImplemented()


@dataclass
class Domain:
    name: str
    provider: Provider

    @property
    def sld(self):
        """
        Second Level Domain (e.g, internal.chat.google.com -> google.com)
        """
        p = tld.parse_tld(self.name, fix_protocol=True)
        return f"{p[1]}.{p[0]}"

    @property
    def dns_name(self):
        """
        After SLD (e.g, internal.chat.google.com -> internal.chat)
        """
        p = tld.parse_tld(self.name, fix_protocol=True)
        p = [x for x in p if x]
        if len(p) == 2:
            return "@"
        return ".".join(p[2:][::-1])

    def update_dns_with_servers(
        self, servers: List[Server], cloud_proxy=True
    ) -> Generator:
        raise NotImplemented()

    def is_active(self, reload=False) -> bool:
        raise NotImplemented()

    def ns_servers(self, reload=False) -> List[str]:
        raise NotImplemented()

    def provision(self) -> Generator:
        raise NotImplemented()
