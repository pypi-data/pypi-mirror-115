import asyncio
import os
import shlex

from .colors import colors


class StreamProtocol(asyncio.subprocess.SubprocessStreamProtocol):
    """
    Capture and dump stout/stderr at the same time
    """
    def pipe_data_received(self, fd, data):
        super().pipe_data_received(fd, data)


def protocol_factory():
    def _p():
        return StreamProtocol(
            limit=asyncio.streams._DEFAULT_LIMIT,
            loop=asyncio.events.get_event_loop()
        )
    return _p


async def run(cmd, *args, verbose=True):
    if verbose or os.getenv('SYSPLAN_TEST'):
        print(''.join([
            colors['gray2bold'],
            '+ ',
            cmd,
            colors['reset'],
        ]))

    if not args:
        args = shlex.split(cmd)

    if os.getenv('SYSPLAN_TEST'):
        return 0, '', ''
    else:
        if verbose:
            loop = asyncio.events.get_event_loop()
            transport, protocol = await loop.subprocess_exec(
                protocol_factory(),
                *args,
            )
            proc = asyncio.subprocess.Process(transport, protocol, loop)
        else:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        stdout, stderr = await proc.communicate()

    if verbose:
        if proc.returncode != 0:
            print(
                colors["redbold"]
                + f'{cmd!r} exited with {proc.returncode}'
                + colors["reset"]
            )
        if stdout:
            print(f'{stdout.decode()}'.strip())
        if stderr:
            print(f'{stderr.decode()}'.strip())

    return proc.returncode, stdout, stderr
