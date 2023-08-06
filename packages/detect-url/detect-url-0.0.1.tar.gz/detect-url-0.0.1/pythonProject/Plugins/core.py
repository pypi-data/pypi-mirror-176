import importlib
import sys

sys.path.append("../")
from settings import settings


class MyApplication:
    # We are going to receive a list of plugins as parameter
    def __init__(self, plugins: list = []):
        # Checking if plugin were sent
        if plugins != []:
            # create a list of plugins
            self._plugins = [
                importlib.import_module(plugin, ".").Plugin() for plugin in plugins
            ]

            for plugin in plugins:
                settings.plugins_names += [plugin, ]

    def run(self):

        # Modified for in order to call process method
        for plugin in self._plugins:
            result = plugin.process(settings.url)
            settings.plugins += [result, ]




