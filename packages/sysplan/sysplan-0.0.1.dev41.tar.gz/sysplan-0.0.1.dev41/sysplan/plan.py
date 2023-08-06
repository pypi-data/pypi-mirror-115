import yaml

from .colors import colors

try:
    import pygments
    import pygments.lexers
    import pygments.formatters
except ImportError:
    pygments = None


class Plan(dict):
    def __init__(self, root, config, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.name = name
        self.config = config

    async def write(self):
        pass

    async def activate(self):
        pass

    async def diff(self):
        pass

    async def destroy(self):
        pass

    async def conf(self):
        desc = ''.join([
            colors['yellowbold'],
            f'[{type(self).__name__}] {self.name}:',
            colors["reset"],
        ])
        conf = yaml.dump(dict(self))
        if pygments:
            conf = pygments.highlight(
                conf,
                pygments.lexers.get_lexer_by_name('YAML'),
                pygments.formatters.get_formatter_by_name('terminal'),
            )

        return '\n'.join([desc, conf])

    @classmethod
    def factory(cls, method, root, config, name, *names):
        for plan_name, plan_data in config.get(name, {}).items():
            if names and plan_name not in names and name not in names:
                continue
            yield cls(root, config, plan_name, **plan_data or {})
