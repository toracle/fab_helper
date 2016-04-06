# -*- coding: utf-8 -*-


def get_user_homedir(user):
    if user == 'root':
        return '/root'
    else:
        return '/home/{}'.format(user)
