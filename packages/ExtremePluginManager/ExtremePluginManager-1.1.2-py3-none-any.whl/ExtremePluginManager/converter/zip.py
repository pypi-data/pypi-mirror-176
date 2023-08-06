import os.path
import shutil
import zipfile

import ExtremePluginManager.constants as constants


def zip_to_directory(src: constants.PATH_TYPEHINT, dst: constants.PATH_TYPEHINT):
    if os.path.isdir(dst):
        shutil.rmtree(dst)

    with zipfile.ZipFile(src, 'r') as zip_ref:
        zip_ref.extractall(dst)
