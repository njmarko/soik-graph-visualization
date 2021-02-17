from django.apps import AppConfig
import pkg_resources


class CoreConfig(AppConfig):
    name = 'core'
    plugins_loading = []
    plugins_visualization = []
    source_index = '0'
    visualization_index = '0'

    graph = None

    def ready(self):
        self.plugins_loading = load_plugins("core.data_source")
        self.plugins_visualization = load_plugins("core.visualization")


def load_plugins(group_name):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=group_name):
        p = ep.load()
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins