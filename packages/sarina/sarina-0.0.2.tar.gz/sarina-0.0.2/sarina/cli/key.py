import click
from rich import box
from rich.table import Table
from sarina.core.logging import console

from .main import cli
from .util import get_cluster


@cli.command(name="keys")
@click.option("--cluster", "-c", "cluster_name", default=None)
@click.pass_context
def keys(ctx, cluster_name):
    cluster = get_cluster(ctx, cluster_name)

    for domain in cluster.domains:
        console.print(f"[bold cyan]{domain.name}:[/bold cyan]")
        print(cluster.template.generate_key(cluster, domain))
        console.print("")
