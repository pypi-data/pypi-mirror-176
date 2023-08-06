import os
import zipfile

import ExtremePluginManager.plugin.base_plugin as base_plugin
from ExtremePluginManager import constants as constants


class ZipFilePlugin(base_plugin.BasePlugin):

    def read_file_bytes(self, path: constants.PATH_TYPEHINT) -> bytes:
        with zipfile.ZipFile(self._path, 'r') as z:
            with z.open(path) as f:
                return f.read()

    def write_file_bytes(self, path: constants.PATH_TYPEHINT, contents: bytes):
        self.remove_file(path)

        with zipfile.ZipFile(self._path, 'a') as z:
            z.writestr(path, contents)

    def remove_file(self, path: constants.PATH_TYPEHINT):
        tmp_name = self._get_tmp_zip_name()

        zin = zipfile.ZipFile(self._path, 'r')
        zout = zipfile.ZipFile(tmp_name, 'w')

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if item.filename != path:
                zout.writestr(item, buffer)

        zout.close()
        zin.close()

        os.remove(self._path)
        os.rename(tmp_name, self._path)

    def _get_tmp_zip_name(self):
        return 'tmp.zip'

    @staticmethod
    def is_plugin_type(path: constants.PATH_TYPEHINT):
        try:
            zipfile.ZipFile(path, 'r').close()
            return True

        except Exception:
            return False
