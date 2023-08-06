import random
from email.generator import Generator

import click
from click import ClickException
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich import box
from rich.table import Table
from sarina.cli.monitoring import monitoring
from sarina.core.logging import console
from sarina.core.task import TaskPool, run_task
from sarina.core.utils import random_string_lower

from .main import cli
from .util import choose_server_provider, current_cluster, get_config, new_progress


@cli.group()
@click.pass_context
def scale(ctx):
    # choose_server_provider(ctx, provider)
    pass


@scale.command(name="up")
@click.option("--provider", "-p", "provider_name", default=None)
@click.argument("count", nargs=1, default=1, type=int)
@click.pass_context
def scale_up(ctx, provider_name, count):
    config = get_config(ctx)
    cluster = current_cluster(ctx)
    provider = choose_server_provider(ctx, provider_name)

    if count > 10:
        raise ClickException("Scaling up limited to at most 10 servers at a time")

    def new_server(name) -> Generator:
        server = yield from provider.create_server(cluster, name)
        yield from cluster.template.provision_server(server)
        return server

    with new_progress() as p:
        pool = TaskPool(progress=p)
        with pool:
            for _ in range(count):
                name = f"{cluster.name}-{random_string_lower(4)}"
                pool.submit(name, new_server(name))

        cluster.servers.extend([s for s in pool.results if s is not None])

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for domain in cluster.domains:
                pool.submit(
                    f"{domain.name}",
                    domain.update_dns_with_servers(cluster.servers),
                )

            if config.monitoring is not None:
                config.monitoring.refresh(config)


@scale.command(name="down")
@click.option("--provider", "-p", "provider_name", default=None)
@click.argument("count", nargs=1, default=1, type=int)
@click.pass_context
def scale_down(ctx, provider_name, count):
    config = get_config(ctx)
    cluster = current_cluster(ctx)

    if provider_name is not None:
        servers = [s for s in cluster.servers if s.provider.name == provider_name]
    else:
        servers = cluster.servers

    if count > len(servers):
        count = len(servers)

    servers = random.sample(servers, count)
    if provider_name is not None:
        console.log(f"Removing {len(servers)} servers from provider '{provider_name}'")
    else:
        console.log(f"Removing {len(servers)} servers")
    for i in range(count):
        cluster.servers.remove(servers[i])

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for domain in cluster.domains:
                pool.submit(
                    domain.name,
                    domain.update_dns_with_servers(cluster.servers),
                )

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for server in servers:
                pool.submit(server.pname, server.destroy())

            if config.monitoring is not None:
                config.monitoring.refresh(config)


@cli.group()
@click.pass_context
def server(ctx):
    pass


@server.command(name="rm")
@click.argument(
    "server_names",
    nargs=-1,
)
@click.pass_context
def remove_server(ctx, server_names):
    config = get_config(ctx)
    cluster = current_cluster(ctx)

    servers = []
    if len(server_names) > 0:
        for s in server_names:
            server = cluster.get_server(name=s)
            if server is None:
                console.error(f"Server {s} not found")
            servers.append(server)
    else:
        answer = prompt(
            {
                "message": "Which servers should I destroy? (You can select multiple server by pressing Space) ",
                "type": "list",
                "multiselect": True,
                "choices": [
                    Choice(
                        name=f"{cluster.servers[s].provider.name}/{cluster.servers[s].name}",
                        value=s,
                    )
                    for s in range(len(cluster.servers))
                ],
            },
        )
        servers = [cluster.servers[s] for s in answer[0]]

    for server in servers:
        cluster.servers.remove(server)

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for domain in cluster.domains:
                pool.submit(
                    domain.name,
                    domain.update_dns_with_servers(cluster.servers),
                )

    with new_progress() as p:
        with TaskPool(progress=p) as pool:
            for server in servers:
                pool.submit(server.pname, server.destroy())

            if config.monitoring is not None:
                config.monitoring.refresh(config)


@server.command(name="ls")
@click.option("--all-clusters", "-a", type=bool, default=False, is_flag=True)
@click.pass_context
def list_servers(ctx, all_clusters):
    config = get_config(ctx)

    table = Table(box=box.SIMPLE_HEAVY, show_header=False, show_footer=False)

    table.add_column("Cloud", justify="right", style="cyan", no_wrap=True)
    table.add_column("Provider", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("IP", style="magenta")

    if all_clusters:
        clusters = config.clusters
    else:
        clusters = [current_cluster(ctx)]

    for cluster in clusters:
        for s in cluster.servers:
            table.add_row(s.provider.cloud, s.provider.name, s.name, s.ip)

    console.print(table)
