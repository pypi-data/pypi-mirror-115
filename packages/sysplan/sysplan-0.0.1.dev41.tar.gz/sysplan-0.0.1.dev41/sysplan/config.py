import importlib_metadata
import os
import yaml


SYSPLAN_ROOT = os.getenv('SYSPLAN_ROOT', '/')
SYSPLAN_D = os.getenv('SYSPLAN_D', '/etc/sysplan.d')


class Config(dict):
    plugins = {
        ep.name: ep
        for ep in importlib_metadata.entry_points(group='sysplan')
    }

    @classmethod
    def factory(cls, root):
        for root, dirs, files in os.walk(root):
            for filename in sorted(files):
                if not filename.endswith('.yaml'):
                    continue
                target_file = os.path.join(root, filename)
                with open(target_file, 'r') as f:
                    content = f.read()
                    for document in content.split('---'):
                        yield cls(yaml.safe_load(document))

    def plans(self, method, root, *names):
        for plugin_name, plans in self.items():
            plugin = None
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name].load()
            elif plugin_name.endswith('.sh'):
                path = os.path.join(SYSPLAN_D, plugin_name)
                if os.path.exists(path):
                    from sysplan.bash import BashPlan
                    plugin = type(
                        plugin_name.capitalize(),
                        (BashPlan,),
                        dict(path=path),
                    )

            if not plugin:
                continue

            plugin_config = self.get(plugin_name, None)
            if plugin_config is None:
                continue

            yield from plugin.factory(method, root, self, plugin_name, *names)
