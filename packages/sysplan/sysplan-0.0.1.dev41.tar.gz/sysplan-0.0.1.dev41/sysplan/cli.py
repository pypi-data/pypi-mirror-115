"""
Apply plans parsed from /etc/sysplan.d/*.yaml.
"""

import contextvars
import cli2
import os

from .config import Config, SYSPLAN_D, SYSPLAN_ROOT


cli = cli2.Group(doc=__doc__)

context = contextvars.ContextVar('context')


async def call(method, config_path, root, *filters):
    for config in Config.factory(SYSPLAN_D):
        for plan in config.plans('diff', SYSPLAN_ROOT, *filters):
            output = await getattr(plan, method)()
            if output:
                print(output)


@cli.cmd(color='green')
async def conf(*plans):
    """
    Dump parsed plans from /etc/sysplan.d/*.yaml.
    """
    await call('conf', SYSPLAN_D, SYSPLAN_ROOT, *plans)


@cli.cmd(color='green')
async def diff(*plans):
    """
    Show diff without applying /etc/sysplan.d/*.yaml.
    """
    await call('diff', SYSPLAN_D, SYSPLAN_ROOT, *plans)


@cli.cmd(color='yellow')
async def test(*plans):
    """
    Dump diffs and commands without touching anything.
    """
    os.environ['SYSPLAN_TEST'] = '1'
    await diff(*plans)
    await activate(*plans)


@cli.cmd(color='yellow')
async def testdestroy(*plans):
    """
    Dump diffs and commands without touching anything.
    """
    os.environ['SYSPLAN_TEST'] = '1'
    await call('destroy', SYSPLAN_D, SYSPLAN_ROOT, *plans)


@cli.cmd
async def apply(*plans):
    """
    Write configuration and execute plan commands.
    """
    await write(*plans)
    await activate(*plans)


@cli.cmd
async def write(*plans):
    """
    Write configuration for plans on the filesystem.
    """
    await call('write', SYSPLAN_D, SYSPLAN_ROOT, *plans)


@cli.cmd
async def activate(*plans):
    """
    Execute plan commands.
    """
    await call('activate', SYSPLAN_D, SYSPLAN_ROOT, *plans)


@cli.cmd(color='red')
async def destroy(*plans):
    """
    Stop, disable, destroy plans.
    """
    await call('destroy', SYSPLAN_D, SYSPLAN_ROOT, *plans)


if __name__ == '__main__':
    cli.entry_point()
