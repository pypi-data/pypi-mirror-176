import base64
import json
import urllib.parse
from dataclasses import dataclass
from uuid import uuid4

from sarina.core.config import Cluster
from sarina.core.task import with_prefix
from sarina.core.utils import PromptField, random_string
from sarina.providers import Domain, Server

from .base import (
    Template,
    script_install_docker,
    script_install_docker_compose,
    tls_crt,
    tls_key,
)


@dataclass
class ShadowsocksV2RayPlugin(Template):
    type = "ss_plugin_v2ray"
    description = "Shadowsocks with V2Ray Plugin"

    password: str = PromptField(default_factory=lambda: random_string(16))
    method: str = PromptField(default="chacha20-ietf-poly1305")

    sarina_dir = "/root/sarina"
    v2ray_path = "/sarina"

    def provision_server(self, server: Server):
        if not server.is_connected:
            yield from with_prefix("Connecting to server", server.connect())

        yield from with_prefix("Installing Docker", server.run(script_install_docker))

        yield from with_prefix(
            "Installing Docker Compose", server.run(script_install_docker_compose)
        )

        yield from with_prefix(
            "Running Services",
            server.run(
                f"""
                    mkdir -p {self.sarina_dir}
                    cd {self.sarina_dir}

                    mkdir cert
                    echo '{tls_crt}' > cert/tls.crt
                    echo '{tls_key}' > cert/tls.key

                    echo '{docker_compose(password=self.password, method=self.method, path=self.v2ray_path)}' > docker-compose.yml
                    echo '{nginx_config(path=self.v2ray_path)}' > nginx.conf
                    docker-compose up -d
                """,
            ),
        )

    def generate_key(self, cluster: Cluster, domain: Domain):
        secret = base64.b64encode(f"{self.method}:{self.password}").decode("utf-8")
        params = {
            "plugin": "v2ray-plugin",
            "path": self.v2ray_path,
            "loglevel": "none",
            "host": domain.name,
        }
        name = f"{cluster.name}-{domain.sld}"
        return f"ss://{secret}@{domain.name}:443/?{urllib.parse.urlencode(params)}&tls#{name}"


docker_compose = (
    lambda path, password, method: """
version: "3"
services:
  shadowsocks:
    image: acrisliu/shadowsocks-libev
    environment:
        - ARGS="--plugin v2ray-plugin --plugin-opts server;path=%s -u"
        - PASSWORD="%s"
        - METHOD="%s"
    restart: always
  wsproxy:
    image: ghcr.io/ghitf/wsproxy:main
    command: ["--backend", "ws://shadowsocks:8388", "--metrics", "0.0.0.0:9900"]
    restart: always
  nginx:
    image: nginx
    restart: always
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./cert:/root/cert
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
""".strip()
    % (path, password, method)
)

nginx_config = (
    lambda path: """
server {
    listen 443 ssl;
    ssl_certificate       /root/cert/tls.crt;
    ssl_certificate_key   /root/cert/tls.key;
    ssl_protocols         TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers           HIGH:!aNULL:!MD5;

    location %s {
      if ($http_upgrade != "websocket") { # Return 404 error when WebSocket upgrading negotiate failed
          return 404;
      }
      proxy_redirect off;
      proxy_pass http://wsproxy;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
      # Show real IP in v2ray access.log
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /metrics {
        proxy_redirect off;
        proxy_pass http://wsproxy:9900;
        proxy_http_version 1.1;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;

    location %s {
      if ($http_upgrade != "websocket") { # Return 404 error when WebSocket upgrading negotiate failed
          return 404;
      }
      proxy_redirect off;
      proxy_pass http://wsproxy;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
      # Show real IP in v2ray access.log
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /metrics {
        proxy_redirect off;
        proxy_pass http://wsproxy:9900;
        proxy_http_version 1.1;
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
""".strip()
    % (path, path)
)
