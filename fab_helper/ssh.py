# -*- coding: utf-8 -*-

import os
import fabric
from fabric import run, put

from fab_helper.util import match_and_delete_n_lines


SSH_CONFIG_ENTRY = '''# Auto-generated entry for {hostname} of {ssh_user}
Host {hostname}
   User {ssh_user}
   IdentityFile {key_path}
   HostName {host_ip}

'''

def ssh_config_entry(user, hostname, local_key_path, ssh_user=None, host_ip=None):
    key_name = local_key_path.rsplit('/')[-1]
    user_home_dir = get_user_homedir(user)
    user_home_ssh_dir = os.path.join(user_home_dir, '.ssh')
    remote_key_path = os.path.join(user_home_ssh_dir, key_name)
    remote_config_path = os.path.join(user_home_ssh_dir, 'config')

    _ssh_user = ssh_user or user
    _host_ip = host_ip or hostname

    if not fabric.contrib.files.exists(user_home_ssh_dir):
        run('mkdir {}'.format(user_home_ssh_dir))

    if fabric.contrib.files.exists(remote_config_path):
        run('chmod 600 {}'.format(remote_config_path))

    comment = '# Auto-generated entry for {hostname} of {ssh_user}'.format(hostname=hostname, ssh_user=_ssh_user)
    match_and_delete_n_lines(remote_config_path, comment, 6)

    put(local_key_path, remote_key_path)
    kwargs = {'ssh_user': _ssh_user, 'hostname': hostname, 'key_path': remote_key_path, 'host_ip': _host_ip}
    fabric.contrib.files.append(remote_config_path, SSH_CONFIG_ENTRY.format(**kwargs))

    run('chmod 400 {}'.format(remote_config_path))


def ssh_known_hosts(hostname):
    run('ssh-keyscan {}'.format(hostname))
