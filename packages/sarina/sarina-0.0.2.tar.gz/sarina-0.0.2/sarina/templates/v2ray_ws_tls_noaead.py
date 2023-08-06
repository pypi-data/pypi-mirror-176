import base64
import json
from dataclasses import dataclass
from uuid import uuid4

from sarina.core.config import Cluster
from sarina.core.task import with_prefix
from sarina.core.utils import PromptField
from sarina.providers import Domain, Server

from .base import (
    Template,
    script_install_docker,
    script_install_docker_compose,
    tls_crt,
    tls_key,
)


@dataclass
class V2RayWSTlsNoAEAD(Template):
    type = "v2ray_ws_tls_noaead"
    description = "V2Ray Websocket+TLS (No AEAD)"

    id: str = PromptField(default_factory=lambda: str(uuid4()))

    sarina_dir = "/root/sarina"
    v2ray_path = "/vipen"

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

                    echo '{docker_compose}' > docker-compose.yml
                    echo '{v2ray_config(id=self.id, path=self.v2ray_path)}' > v2ray.json
                    echo '{nginx_config(path=self.v2ray_path)}' > nginx.conf
                    docker-compose up -d
                """,
            ),
        )

    def generate_key(self, cluster: Cluster, domain: Domain):
        key_data = {
            "add": domain.name,
            "aid": "0",
            "alpn": "",
            "host": domain.name,
            "id": self.id,
            "net": "ws",
            "path": self.v2ray_path,
            "port": "443",
            "ps": f"{cluster.name}-{domain.sld}",
            "scy": "none",
            "sni": domain.name,
            "tls": "tls",
            "type": "",
            "v": "2",
        }
        return f"vmess://{base64.b64encode(json.dumps(key_data).encode('utf-8')).decode('utf-8')}"


docker_compose = """
version: "3"
services:
  v2ray:
    image: v2fly/v2fly-core
    command: ["run", "-c", "/etc/v2ray/config.json"]
    restart: always
    environment:
      - V2RAY_VMESS_AEAD_FORCED=false
    volumes:
      - ./v2ray.json:/etc/v2ray/config.json:ro
  wsproxy:
    image: ghcr.io/ghitf/wsproxy:main
    command: ["--backend", "ws://v2ray:6000", "--metrics", "0.0.0.0:9900"]
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

v2ray_config = (
    lambda id, path: """
{
    "inbounds": [{
        "port": 6000,
        "listen": "0.0.0.0",
        "protocol": "vmess",
        "settings": {
            "clients": [{
                "id": "%s",
                "alterId": 64
            }]
        },
        "streamSettings": {
            "network": "ws",
            "wsSettings": {
                "path": "%s"
            }
        }
    }],
    "outbounds": [{
        "protocol": "freedom",
        "settings": {}
    }]
}
""".strip()
    % (id, path)
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
