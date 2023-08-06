import asyncio
import os
import shlex
import sys

from .colors import colors
from .plan import Plan

try:
    import pygments
    import pygments.lexers
    import pygments.formatters
except ImportError:
    pygments = None


def transpile(src, prefix=None, output=None):
    output = output or []
    prefix = prefix or ''

    if isinstance(src, dict):
        for key, value in src.items():
            prefix_key = key
            if prefix:
                prefix_key = '_'.join([prefix, key])
            output = transpile(value, prefix_key, output)
    elif isinstance(src, list):
        for num, value in enumerate(src):
            output = transpile(value, f'{prefix}_{num}', output)
    elif isinstance(src, int):
        output.append(f'{prefix}={src}')
    elif isinstance(src, str):
        output.append(f'{prefix}={shlex.quote(src)}')

    return output


class BashPlan(Plan):
    def content(self):
        with open(self.path, 'r') as f:
            content = f.read()
        variables = [
            f'plan_name="{self.name}"',
        ]
        variables += transpile(self)
        content = '\n'.join(variables) + f'\n{content}'
        return content

    async def write(self):
        return await self.call('write')

    async def activate(self):
        return await self.call('activate')

    async def diff(self):
        return await self.call('diff')

    async def destroy(self):
        return await self.call('destroy')

    async def call(self, function):
        content = self.content() + f'\n{function}\n'
        print(''.join([
            colors['gray2bold'],
            f'+ {self.name}: {self.path} {function}',
            colors['reset'],
        ]))

        if function != 'diff' and os.environ.get('SYSPLAN_TEST'):
            return ''

        proc = await asyncio.create_subprocess_exec(
            '/bin/bash',
            '-c',
            content,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        stdout, stderr = await proc.communicate()
        return (stdout or b'').decode('utf8') + (stderr or b'').decode('utf8')

    async def conf(self):
        desc = ''.join([
            colors['yellowbold'],
            f'[{type(self).__name__}] {self.name}:',
            colors["reset"],
        ])
        conf = [
            f'plan_name="{self.name}"',
        ]
        conf += transpile(self)
        if pygments:
            conf = pygments.highlight(
                '\n'.join(conf),
                pygments.lexers.get_lexer_by_name('bash'),
                pygments.formatters.get_formatter_by_name('terminal'),
            )

        return '\n'.join([desc, conf])
