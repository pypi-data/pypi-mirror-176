import click
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich import box
from rich.table import Table
from sarina.core.config import Cluster
from sarina.core.logging import console
from sarina.core.utils import prompt_factory

from .main import cli
from .util import get_config


@cli.group()
def cluster():
    pass


@cluster.command(name="add")
@click.argument("cluster_name", nargs=1, default="")
@click.pass_context
def add_cluster(ctx, cluster_name):
    config = get_config(ctx)

    if not cluster_name:
        answer = prompt(
            {
                "message": "Enter Cluster Name",
                "type": "input",
                "validate": lambda v: v and " " not in v,
            },
        )
        cluster_name = answer[0]

    if config.get_cluster(cluster_name) is not None:
        console.error(f"Cluster with name '{cluster_name}' already exists")
        return

    cluster = Cluster.new(cluster_name)

    answer = prompt(
        {
            "message": "Select Template to use in Cluster",
            "type": "rawlist",
            "choices": [
                Choice(name=f"{t.description}", value=t) for t in config.template_cls
            ],
        },
    )
    template_cls = answer[0]

    params = prompt(prompt_factory(template_cls))
    template = template_cls(type=template_cls.type, **params)
    cluster.template = template

    config.clusters.append(cluster)
    console.log(f"Created new cluster '{cluster_name}'")

    if not config.current_cluster:
        config.current_cluster = cluster
        console.log(f"Set '{cluster_name}' as default cluster")
    else:
        console.log(f"To use this cluster by default run <TODO>")


@cluster.command(name="rm")
@click.argument(
    "cluster_name",
    nargs=1,
)
@click.pass_context
def remove_cluster(ctx, cluster_name):
    config = get_config(ctx)

    cluster = config.get_cluster(cluster_name)
    if cluster is None:
        console.error(f"Cluster {cluster_name} not found")
        return

    console.log("Removing cluster will not destroy it's resources.")
    console.log("Make sure you scale down the cluster before continuing.")

    answer = prompt(
        {
            "message": "Do you wish to continue?",
            "type": "confirm",
            "default": False,
        },
    )
    if not answer[0]:
        return

    config.clusters.remove(cluster)
    console.log(f"Cluster '{cluster_name}' removed")


@cluster.command(name="ls")
@click.pass_context
def list_clusters(ctx):
    config = get_config(ctx)

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, show_footer=False)

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Template", justify="right", style="cyan", no_wrap=True)
    table.add_column("Server Count", style="magenta")
    table.add_column("Domain Count", style="magenta")

    for c in config.clusters:
        table.add_row(c.name, c.template.type, str(len(c.servers)), str(len(c.domains)))

    console.print(table)


@cluster.command(name="use")
@click.argument("cluster_name", nargs=1, default="")
@click.pass_context
def use_cluster(ctx, cluster_name):
    config = get_config(ctx)

    if not cluster_name:
        answer = prompt(
            {
                "message": "Choose Cluster",
                "type": "rawlist",
                "choices": [c.name for c in config.clusters],
            },
        )
        cluster_name = answer[0]

    cluster = config.get_cluster(cluster_name)
    if cluster is None:
        console.error(f"Cluster {cluster_name} not found")
        return

    config.current_cluster = cluster
    console.log(f"Set '{cluster.name}' as default cluster")
