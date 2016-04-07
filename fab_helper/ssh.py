# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import fabric
from fabric.api import run, put, sudo

from fab_helper.util import match_and_delete_n_lines
from fab_helper.path import get_user_homedir


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

    run_cmd = sudo if user == 'root' else run
    _ssh_user = ssh_user or user
    _host_ip = host_ip or hostname
    sudo_kwargs = {}
    if user == 'root':
        sudo_kwargs = {'use_sudo': True}

    if not fabric.contrib.files.exists(user_home_ssh_dir, use_sudo=True):
        run_cmd('mkdir {}'.format(user_home_ssh_dir))

    if fabric.contrib.files.exists(remote_config_path, use_sudo=True):
        run_cmd('chmod 600 {}'.format(remote_config_path))

    comment = '# Auto-generated entry for {hostname} of {ssh_user}'.format(hostname=hostname, ssh_user=_ssh_user)
    match_and_delete_n_lines(remote_config_path, comment, 6)

    if not fabric.contrib.files.exists(remote_key_path, use_sudo=True):
        put(local_key_path, remote_key_path, **sudo_kwargs)
    run_cmd('chmod 400 {}'.format(remote_key_path))

    kwargs = {'ssh_user': _ssh_user, 'hostname': hostname, 'key_path': remote_key_path, 'host_ip': _host_ip}
    fabric.contrib.files.append(remote_config_path, SSH_CONFIG_ENTRY.format(**kwargs), **sudo_kwargs)

    run_cmd('chmod 400 {}'.format(remote_config_path))


ADD_KNOWN_HOST = '''if [ -z "`ssh-keygen -F {ip}`" ] ; then
  ssh-keyscan -H {ip} >> {known_hosts_path}
fi
'''

def ssh_known_hosts(hostname, known_hosts_path='~/.ssh/known_hosts', run_cmd=run):
    if fabric.contrib.files.exists(known_hosts_path, use_sudo=True):
        run_cmd('chmod 644 {}'.format(known_hosts_path))
    run_cmd(ADD_KNOWN_HOST.format(ip='bitbucket.org', known_hosts_path=known_hosts_path))
    run_cmd('chmod 400 {}'.format(known_hosts_path))
