import shutil

import ExtremePluginManager.constants as constants


def directory_to_zip(src: constants.PATH_TYPEHINT, dst: constants.PATH_TYPEHINT, zip_format: str = "zip"):
    """
    Supported Formats: "zip", "tar", "gztar","bztar", or "xztar"
    """
    if dst.endswith(".{}".format(zip_format)):
        dst = dst.replace(".{}".format(zip_format), "")

    shutil.make_archive(dst, zip_format, src)
