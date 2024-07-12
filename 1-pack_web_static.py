#!/usr/bin/python3
"""
    Python Script Use Fabric Library to generate a achrive file
"""
from fabric.api import local
from datetime import datetime
from os import makedirs, path


def do_pack():
    """
        Function Generate tgz archive file
    """
    try:
        if not path.exists('versions'):
            makedirs('versions')

        date = datetime.now()
        f_date = date.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(f_date)

        tar_result = local("tar -cvzf {} web_static".format(archive_path))

        if tar_result.failed:
            return None
        else:
            return archive_path
    except Exception:
        return None
