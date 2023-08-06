"""Asset of type .APK package file.
This module takes care of preparing a file of type .APK before injecting it to the runtime instance.
"""
import io
import logging
from typing import List

import click

from ostorlab.assets import android_apk as android_apk_asset
from ostorlab.cli.scan.run import run

logger = logging.getLogger(__name__)


@run.run.command()
@click.argument('files', type=click.File(mode='rb'), nargs=-1, required=True)
@click.pass_context
def android_apk(ctx: click.core.Context, files: List[io.FileIO]) -> None:
    """Run scan for android .APK package file."""
    runtime = ctx.obj['runtime']
    assets = []
    for f in files:
        assets.append(android_apk_asset.AndroidApk(content=f.read(), path=str(f.name)))
    logger.debug('scanning assets %s', [str(asset) for asset in assets])
    runtime.scan(title=ctx.obj['title'], agent_group_definition=ctx.obj['agent_group_definition'], assets=assets)
