import click
from rich import box
from rich.table import Table
from sarina.core.config import Cluster
from sarina.core.logging import console
from sarina.core.task import run_task

from .main import cli
from .util import choose_cdn_provider, current_cluster, new_progress


@cli.group()
def domain():
    pass


@domain.command(name="add")
@click.option("--provider", "-p", default=None)
@click.argument(
    "domain_name",
    nargs=1,
)
@click.pass_context
def add_domain(ctx, provider, domain_name):
    cluster = current_cluster(ctx)
    cdn_provider = choose_cdn_provider(ctx, provider)

    def provision(domain_name):
        domain = yield from cdn_provider.create_domain(domain_name)
        yield from domain.provision()
        yield from domain.update_dns_with_servers(cluster.servers)
        return domain

    with new_progress() as p:
        domain = run_task(domain_name, provision(domain_name), progress=p)

    if domain:
        cluster.domains.append(domain)


@domain.command(name="rm")
@click.argument(
    "domain_name",
    nargs=1,
)
@click.pass_context
def remove_domain(ctx, domain_name):
    cluster: Cluster = current_cluster(ctx)

    domain = cluster.get_domain(domain_name)
    if domain is None:
        console.error(f"Domain {domain_name} not found")
        return

    console.log(f"Removing domain '{domain_name}'.")
    console.log(
        "This only removes it from the cluster config, if you want it removed from the provider you must do that manually."
    )
    cluster.domains.remove(domain)


@domain.command(name="ls")
@click.pass_context
def list_domains(ctx):
    cluster: Cluster = current_cluster(ctx)

    table = Table(box=box.SIMPLE_HEAVY, show_header=False, show_footer=False)

    table.add_column("Cloud", justify="right", style="cyan", no_wrap=True)
    table.add_column("Provider", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")

    for domain in cluster.domains:
        table.add_row(domain.provider.cloud, domain.provider.name, domain.name)

    console.print(table)
