import os

import yaml
from sarina.core.task import with_prefix
from sarina.core.utils import dataclass
from sarina.providers import Server
from sarina.providers.base import Domain
from sarina.templates.base import script_install_docker, script_install_docker_compose


@dataclass
class Monitoring:
    server: Server
    domain: Domain

    monitoring_dir = "/root/monitoring"

    def provision_server(self, config):
        server, domain = self.server, self.domain

        if not server.is_connected:
            yield from with_prefix("Connecting to server", server.connect())

        yield from with_prefix("Installing Docker", server.run(script_install_docker))

        yield from with_prefix(
            "Installing Docker Compose", server.run(script_install_docker_compose)
        )

        yield from with_prefix(
            f"Fetching certificates for {domain.name}",
            server.run(
                f"""
                mkdir -p {self.monitoring_dir}
                cd {self.monitoring_dir}

                docker run --rm  -it  \
                    -v "{self.monitoring_dir}/acme":/acme.sh \
                    neilpang/acme.sh --register-account -m me@"{domain.sld}"

                docker run --rm  -it  \
                    --net=host \
                    -v "{self.monitoring_dir}/acme":/acme.sh \
                    neilpang/acme.sh  --issue -d {domain.name} --standalone
                res=$?
                if [ $res -eq 2 ]; then
                    echo "Certificates already exist"
                elif [ $res -ne 0 ]; then
                    exit $res
                fi

                mkdir {self.monitoring_dir}/cert
                cp {os.path.join(self.monitoring_dir, "acme", domain.name, "fullchain.cer")} {self.monitoring_dir}/cert/tls.crt
                cp {os.path.join(self.monitoring_dir, "acme", domain.name, f"{domain.name}.key")} {self.monitoring_dir}/cert/tls.key
                """
            ),
        )

        yield from self.refresh(config)

    def refresh(self, config):
        server, domain = self.server, self.domain

        prom_targets = []
        for cluster in config.clusters:
            for s in cluster.servers:
                prom_targets.append(
                    {
                        "targets": [s.ip],
                        "labels": {
                            "ip": s.ip,
                            "server": s.name,
                            "provider": s.provider.name,
                            "cluster": cluster.name,
                        },
                    }
                )

        from .dashboard_overview import dashboard as overview_dashboard
        from .dashboard_traffic import dashboard as traffic_dashboard

        yield from with_prefix(
            "Copying dashboard configurations",
            server.run(
                f"""
                    cd {self.monitoring_dir}

                    mkdir -p grafana/datasources grafana/dashboards
                    echo '{grafana_datasource}' > grafana/datasources/datasource.yaml
                    echo '{grafana_dashboard}' > grafana/dashboards/dashboard.yaml
                    echo '{overview_dashboard}' > grafana/dashboards/overview.json
                    echo '{traffic_dashboard}' > grafana/dashboards/traffic.json
                """,
            ),
        )

        yield from with_prefix(
            "Running Services",
            server.run(
                f"""
                    cd {self.monitoring_dir}
                    echo '{docker_compose}' > docker-compose.yml
                    echo '{prom_conf(prom_targets)}' > prometheus.yaml
                    echo '{nginx_config(domain=domain.name)}' > nginx.conf
                    docker-compose up -d
                """,
            ),
        )


docker_compose = """
version: "3"
services:
  prometheus:
    image: prom/prometheus:v2.40.1
    restart: always
    ports:
      - 9090:9090
    volumes:
      - ./prometheus.yaml:/etc/prometheus/prometheus.yml
      - prometheus:/prometheus
  grafana:
    image: grafana/grafana:8.2.6
    ports:
      - 3000:3000
    restart: always
    volumes:
      - grafana:/var/lib/grafana
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
  nginx:
    image: nginx
    restart: always
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./cert:/root/cert
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
volumes:
  grafana:
  prometheus:
""".strip()


prom_conf = lambda targets: yaml.safe_dump(
    {
        "global": {"scrape_interval": "15s", "evaluation_interval": "15s"},
        "scrape_configs": [
            {
                "job_name": "sarina-server",
                "relabel_configs": [
                    {
                        "source_labels": ["server"],
                        "target_label": "instance",
                    },
                ],
                "static_configs": targets,
            }
        ],
    }
)

nginx_config = (
    lambda domain: """
server {
    listen 443 ssl;
    server_name %s;
    ssl_certificate       /root/cert/tls.crt;
    ssl_certificate_key   /root/cert/tls.key;
    ssl_protocols         TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers           HIGH:!aNULL:!MD5;

    location / {
        proxy_redirect off;
        proxy_pass http://grafana:3000;
        proxy_http_version 1.1;
    }
}

server {
    listen 80 default_server;
    server_name %s;
    return 301 https://$host$request_uri;
}
""".strip()
    % (domain, domain)
)

grafana_datasource = """
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
""".strip()

grafana_dashboard = """
apiVersion: 1
providers:
  - name: 'Default'
    folder: 'sarina'
    options:
      path: /etc/grafana/provisioning/dashboards
""".strip()
