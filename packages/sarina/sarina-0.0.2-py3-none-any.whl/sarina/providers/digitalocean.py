import os
import time
from email.generator import Generator
from typing import List

from sarina.core.config import Cluster
from sarina.core.logging import console
from sarina.core.task import with_prefix
from sarina.core.utils import (
    PromptField,
    dataclass,
    ssh_key_fingerprint,
    ssh_key_public_key,
)

import digitalocean

from .base import CDNProvider, ProviderError, Server, ServerProvider


@dataclass
class DigitalOceanServer(Server):
    def destroy(self) -> Generator:
        yield ("Destroying droplet")
        droplet = self.provider.api.get_droplet(self.id)
        droplet.destroy()


@dataclass
class DigitalOceanProvider(ServerProvider, CDNProvider):
    cloud = "DigitalOcean"
    server_cls = DigitalOceanServer

    api_key: str = PromptField()
    project: str = PromptField(required=False)

    _manager = None

    def init_provider(self):
        if not self.ssh_key:
            raise ProviderError("SSH key not specified")
        if not os.path.exists(self.ssh_key_path):
            raise ProviderError(f"SSH Key '{self.ssh_key}' doesn't exist")

        yield "Checking SSH key exists on DigitalOcean"
        key = self.fetch_ssh_key()

        if key is None:
            console.warn(f"SSH key '{self.ssh_key}' not found in DigitalOcean account")
            yield f"Adding SSH key '{self.ssh_key}' to DigitalOcean"
            key = digitalocean.SSHKey(
                token=self.api.token,
                name="sarina",
                public_key=ssh_key_public_key(self.ssh_key_path),
            )
            key.create()
            console.log(f"Created new SSH key {key.id}")

    def create_server(self, cluster: Cluster, name: str):
        yield f"Creating droplet '{name}'"
        droplet = digitalocean.Droplet(
            token=self.api.token,
            name=name,
            region="fra1",
            image="ubuntu-20-04-x64",
            size_slug="s-1vcpu-512mb-10gb",
            ssh_keys=[self.fetch_ssh_key()],
            backups=False,
            tags=[self.cluster_tag(cluster)],
        )
        droplet.create()

        yield f"Waiting for droplet to be ready"
        timeout = 60
        for i in range(timeout):
            time.sleep(1)
            droplet.load()
            if droplet.status == "active":
                break
            yield f"Waiting for droplet to be ready [{i+1}/{timeout}s]"
        else:
            droplet.destroy()
            raise ProviderError("Droplet creation timed out")

        server = self.droplet_to_server(droplet)

        # Wait for the server to finish updating and installing stuff on first boot
        # https://www.digitalocean.com/community/questions/solved-how-to-wait-for-droplet-agent-to-be-installed-to-avoid-apt-lock-issues
        yield from with_prefix("Connecting to server", server.connect())
        yield from with_prefix(
            "Waiting for server to chill",
            server.run(
                """
                for ((i=1;i<=60;i++)); do
                    echo "[$i/60s]"
                    if ls /etc/systemd/system/droplet-agent.services &> /dev/null; then
                        break
                    fi
                    sleep 1
                done
                """
            ),
            style=None,
        )

        return server

    @property
    def api(self):
        if self._manager is None:
            self._manager = digitalocean.Manager(token=self.api_key)
        return self._manager

    def fetch_cluster_servers(self, cluster: Cluster) -> List[DigitalOceanServer]:
        return [
            self.droplet_to_server(d)
            for d in self.api.get_all_droplets(tag_name=self.cluster_tag(cluster))
        ]

    def fetch_server(self, id: str) -> Server:
        try:
            return self.droplet_to_server(self.api.get_droplet(id))
        except digitalocean.NotFoundError:
            return None

    def fetch_ssh_key(self) -> digitalocean.SSHKey:
        fingerprint = ssh_key_fingerprint(self.ssh_key_path)
        for k in self.api.get_all_sshkeys():
            if k.fingerprint == fingerprint:
                return k
        return None

    def cluster_tag(self, cluster: Cluster):
        return f"sarina-{cluster.name}"

    def droplet_to_server(self, droplet) -> DigitalOceanServer:
        return self.server_cls(
            provider=self, name=droplet.name, ip=droplet.ip_address, id=droplet.id
        )
