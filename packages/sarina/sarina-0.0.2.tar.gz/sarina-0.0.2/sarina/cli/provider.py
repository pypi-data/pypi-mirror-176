import click
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich import box
from rich.table import Table
from sarina.core.logging import console
from sarina.core.task import run_task
from sarina.core.utils import prompt_factory

from .main import cli
from .util import get_config, new_progress


@cli.group()
def provider():
    pass


@provider.command(name="add")
@click.argument("provider_name", nargs=1, default="")
@click.pass_context
def add_provider(ctx, provider_name):
    config = get_config(ctx)

    answer = prompt(
        {
            "message": "Select Provider Cloud",
            "type": "rawlist",
            "choices": [
                Choice(name=f"{p.cloud}", value=p) for p in config.provider_cls
            ],
        },
    )
    provider_cls = answer[0]

    if not provider_name:
        answer = prompt(
            {
                "message": "Enter Provider Name",
                "type": "input",
                "validate": lambda v: v and " " not in v,
            },
        )
        provider_name = answer[0]
    if config.get_provider(provider_name) is not None:
        console.error(f"Provider with name {provider_name} already exists")
        return

    params = prompt(prompt_factory(provider_cls))
    provider = provider_cls(cloud=provider_cls.cloud, name=provider_name, **params)

    with new_progress() as p:
        run_task(provider.name, provider.init_provider(), progress=p)

    config.providers.append(provider)

    console.log(f"New provider '{provider_name}' created")


@provider.command(name="rm")
@click.argument(
    "provider_name",
    nargs=1,
)
@click.pass_context
def remove_provider(ctx, provider_name):
    config = get_config(ctx)

    provider = config.get_provider(provider_name)
    if provider is None:
        console.error(f"Provider {provider_name} not found")
        return

    config.providers.remove(provider)
    console.log(f"Provider '{provider_name}' removed")


@provider.command(name="ls")
@click.option("--show-api-key", "-a", type=bool, is_flag=True, default=False)
@click.pass_context
def list_providers(ctx, show_api_key):
    config = get_config(ctx)

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, show_footer=False)

    table.add_column("Cloud", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Supports Servers", style="magenta")
    table.add_column("Supports Domains", style="magenta")
    if show_api_key:
        table.add_column("API Key", style="magenta")

    bool_str = lambda b: "yes" if b else "no"
    for p in config.providers:
        f = [p.cloud, p.name, bool_str(p.can_server), bool_str(p.can_cdn)]
        if show_api_key:
            f.append(p.api_key)
        table.add_row(*f)

    console.print(table)
