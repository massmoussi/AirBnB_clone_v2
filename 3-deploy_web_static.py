#!/usr/bin/python3
"""
    Python Script Automate the deployement Process
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os import makedirs, path
from pathlib import Path

env.hosts = ['18.206.208.103', '52.201.192.84']


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


def do_deploy(archive_path):
    """
    Function deploy the Code to the server
        archive_path: path of the Code files
    """
    file_path = Path(archive_path)
    if not file_path.is_file():
        return False
    try:
        n_ext = archive_path.split("/")[-1]
        name = n_ext.split(".")[0]
        new = "/data/web_static/releases/{}".format(name)
        put(archive_path, "/tmp/")
        run("mkdir {}".format(new))
        run("tar -xzf /tmp/{} -C {}".format(n_ext, new))
        run("rm /tmp/{}".format(n_ext))
        run("mv {}/web_static/* {}".format(new, new))
        run("rm /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new))
        return True
    except Exception:
        return False


def deploy():
    """
        Full deployement , Call other functions
    """
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)
