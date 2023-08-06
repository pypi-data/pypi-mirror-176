import dataclasses
import os

import click
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from sarina.core.config import Cluster, Config, Monitoring
from sarina.core.logging import console
from sarina.core.task import TaskPool, run_task, with_prefix
from sarina.templates.base import script_install_docker, script_install_docker_compose

from .main import cli
from .util import choose_server_provider, current_cluster, get_config, new_progress


@cli.group()
def monitoring():
    pass


@monitoring.command(name="init")
@click.option("--provider", "-p", "provider_name", default=None)
@click.pass_context
def init_monitoring(ctx, provider_name):
    config: Config = get_config(ctx)
    provider = choose_server_provider(ctx, provider_name)

    if config.monitoring is not None:
        console.error("Monitoring has already been initialized.")
        console.error(
            "Consider destroying the current configuration if you want to reinitialize."
        )
        return

    candidate_domains = [
        dataclasses.replace(d, name=f"monitoring.{d.sld}")
        for d in config.get_all_domains()
    ]

    if len(candidate_domains) == 0:
        console.error("Cannot init monitoring until you have added at least one domain")
        return

    answer = prompt(
        {
            "message": "Which domain do you want to use?",
            "type": "rawlist",
            "choices": [
                Choice(name=candidate_domains[d].name, value=d)
                for d in range(len(candidate_domains))
            ],
        },
    )
    domain = candidate_domains[answer[0]]

    with new_progress() as p:
        server = run_task(
            "Monitoring Server",
            provider.create_server(Cluster.new("monitoring"), "monitoring"),
            progress=p,
        )

    if server is None:
        return

    with new_progress() as p:
        run_task(
            domain.name,
            domain.update_dns_with_servers([server], cloud_proxy=False),
            progress=p,
        )

    monitoring = Monitoring(server=server, domain=domain)
    with new_progress() as p:
        run_task(
            server.name,
            monitoring.provision_server(config),
            progress=p,
        )

    config.monitoring = monitoring


@monitoring.command(name="destroy")
@click.pass_context
def destroy_monitoring(ctx):
    config = get_config(ctx)

    if config.monitoring is None:
        console.log("No monitoring configration exists")
        return

    server = config.monitoring.server
    domain = config.monitoring.domain
    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            if server is not None:
                pool.submit(server.pname, server.destroy())
            if domain is not None:
                pool.submit(domain.name, domain.update_dns_with_servers([]))
