from .plan import Plan
from .run import run


class DockerConfig:
    @classmethod
    def factory(cls, method, root, config, name, *filters):
        for volume in config[name].get('volumes', []):
            if filters and volume not in filters and 'docker' not in filters:
                continue
            yield DockerVolumePlan(
                root,
                config,
                volume,
                **config[name]['volumes'][volume] or {},
            )

        for network in config[name].get('networks', []):
            if filters and network not in filters and 'docker' not in filters:
                continue
            yield DockerNetworkPlan(
                root,
                config,
                network,
                **config[name]['networks'][network] or {},
            )


class DockerPlan(Plan):
    async def start(self):
        rc, out, err = await run('systemctl is-active docker', verbose=False)
        if out.strip() == b'active':
            return
        await run('systemctl start docker')


class DockerResourcePlan(DockerPlan):
    resource = None

    async def exists(self):
        rc, out, err = await run(
            f'docker {self.resource} ls -q --filter name={self.name}',
            verbose=False,
        )
        return len(out.strip()) > 1

    async def write(self):
        pass

    async def activate(self):
        await super().start()
        if not await self.exists():
            cmd = f'docker {self.resource} create {self.name}'
            rc, out, err = await run(cmd)

    async def diff(self):
        if not await self.exists():
            return f'+ docker {self.resource} create {self.name}'

    async def destroy(self):
        await super().start()
        if await self.exists():
            rc, out, err = await run(f'docker {self.resource} rm {self.name}')


class DockerNetworkPlan(DockerResourcePlan):
    resource = 'network'


class DockerVolumePlan(DockerResourcePlan):
    resource = 'volume'
