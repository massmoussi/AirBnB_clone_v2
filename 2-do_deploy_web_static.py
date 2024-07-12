#!/usr/bin/python3
""" Generale DOcumentation """

from fabric.api import env, put, run
from pathlib import Path

env.hosts = ['18.206.208.103', '52.201.192.84']


def do_deploy(archive_path):
    """ Documentation """
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
