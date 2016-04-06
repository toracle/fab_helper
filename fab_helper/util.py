# -*- coding: utf-8 -*-

import fabric
from fabric.api import run
import fabtools


def install_python_devel():
    fabtools.rpm.groupinstall('Development Tools')
    fabtools.rpm.install('python-devel')


def match_and_delete_n_lines(remote_path, pattern, num_lines):
    if fabric.contrib.files.exists(remote_path):
        run("sed -i -e '/{pattern}/,+{num_lines}d' {remote_path}".format(pattern=pattern, remote_path=remote_path, num_lines=num_lines))
