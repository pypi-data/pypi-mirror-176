from click import ClickException, Context
from InquirerPy import prompt
from InquirerPy.base.control import Choice
from rich.progress import Progress, SpinnerColumn, TextColumn
from sarina.core.config import Cluster, Config
from sarina.core.logging import console
from sarina.providers.base import CDNProvider, ServerProvider


def new_progress():
    return Progress(
        SpinnerColumn(),
        TextColumn(
            "[blue]{task.description}:[/blue] {task.fields[message]}",
            justify="left",
        ),
        console=console,
    )


def get_config(ctx: Context) -> Config:
    return ctx.obj["config"]


def current_cluster(ctx: Context) -> Cluster:
    cfg = get_config(ctx)
    if cfg.current_cluster is None:
        raise ClickException("No cluster has been selected")
    return cfg.current_cluster


def get_cluster(ctx: Context, cluster_name: str = None) -> Cluster:
    cfg = get_config(ctx)
    if cluster_name is None:
        if cfg.current_cluster is None:
            raise ClickException("No cluster has been selected")
        return cfg.current_cluster
    cluster = cfg.clusters.get_cluster(cluster_name)
    if cluster is None:
        raise ClickException(f"Cluster '{cluster_name}' does not exist")
    return cluster


def choose_server_provider(ctx: Context, name=None) -> ServerProvider:
    cfg = get_config(ctx)

    if name is not None:
        if name not in cfg.providers:
            raise ClickException(f"Provider '{name}' does not exist")
        return cfg.providers[name]

    provider = None
    server_providers = cfg.server_providers
    if len(server_providers) == 0:
        raise ClickException(f"No server providers found")
    elif len(server_providers) == 1:
        provider = server_providers[0]
    else:
        answer = prompt(
            {
                "message": "Select server provider:",
                "type": "fuzzy",
                "choices": [
                    Choice(name=f"{p.cloud} - {p.name}", value=pid)
                    for pid, p in enumerate(server_providers)
                ],
            },
        )
        provider = server_providers[answer[0]]

    ctx.obj["server_provider"] = provider
    return provider


def choose_cdn_provider(ctx: Context, name=None) -> CDNProvider:
    cfg = get_config(ctx)

    if name is not None:
        if name not in cfg.providers:
            raise ClickException(f"Provider '{name}' does not exist")
        return cfg.providers[name]

    provider = None
    cdn_providers = cfg.cdn_providers
    if len(cdn_providers) == 0:
        raise ClickException(f"No CDN providers found")
    elif len(cdn_providers) == 1:
        provider = cdn_providers[0]
    else:
        answer = prompt(
            {
                "message": "Select CDN provider:",
                "type": "fuzzy",
                "choices": [
                    Choice(name=f"{p.cloud} - {p.name}", value=p) for p in cdn_providers
                ],
            },
        )
        provider = answer[0]

    ctx.obj["cdn_provider"] = provider
    return provider


def get_server_provider(ctx: Context) -> ServerProvider:
    provider = ctx.obj.get("server_provider", None)
    if provider is None:
        raise ClickException("Server provider not selected")
    return provider


def get_cdn_provider(ctx: Context) -> CDNProvider:
    provider = ctx.obj.get("cdn_provider", None)
    if provider is None:
        raise ClickException("CDN provider not selected")
    return provider
