import os

import click
from click import ClickException
from sarina.core.config import DEFAULT_CONFIG_DIR, ConfigError, load_config
from sarina.core.logging import console

from .util import get_config


@click.group()
@click.option(
    "--config", "config_path", default=os.path.join(DEFAULT_CONFIG_DIR, "config.yaml")
)
@click.option("--cluster", "-c", default=None)
@click.pass_context
def cli(ctx, config_path, cluster):
    from sarina.providers.arvan import ArvanProvider
    from sarina.providers.digitalocean import DigitalOceanProvider
    from sarina.templates.ss_v2ray_plugin import ShadowsocksV2RayPlugin
    from sarina.templates.v2ray_ws_tls_noaead import V2RayWSTlsNoAEAD

    if not os.path.exists(DEFAULT_CONFIG_DIR):

        # Temporary fix
        old_path = os.path.expanduser("~/.vipen")
        if os.path.exists(old_path):
            import shutil

            console.log("Migrating config from vipen")
            shutil.copytree(old_path, DEFAULT_CONFIG_DIR)

        os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)

    ctx.obj = {}

    try:
        ctx.obj["config"] = load_config(
            config_path,
            use_cluster=cluster,
            provider_cls=[DigitalOceanProvider, ArvanProvider],
            template_cls=[V2RayWSTlsNoAEAD, ShadowsocksV2RayPlugin],
        )
    except ConfigError as e:
        raise ClickException(str(e))


@cli.result_callback()
@click.pass_context
def save_config(ctx, *args, **kwargs):
    get_config(ctx).save(kwargs.get("config_path"))
