import os.path

import ExtremePluginManager.plugin.base_plugin as base_plugin
from ExtremePluginManager import constants as constants


class DirectoryPlugin(base_plugin.BasePlugin):
    @staticmethod
    def is_plugin_type(path: constants.PATH_TYPEHINT):
        return os.path.isdir(path)

    def _get_path(self, path: str) -> str:
        return os.path.join(self._path, path)

    def read_file_bytes(self, path: constants.PATH_TYPEHINT) -> bytes:
        with open(self._get_path(path), 'rb') as f:
            return f.read()

    def write_file_bytes(self, path: constants.PATH_TYPEHINT, contents: bytes):
        with open(self._get_path(path), 'wb') as f:
            f.write(contents)

    def remove_file(self, path: constants.PATH_TYPEHINT):
        os.remove(self._get_path(path))
