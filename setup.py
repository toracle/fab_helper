#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


setup(
    name='fab_helper',
    version='0.0.2',
    description=u'',
    author='Jeongsoo Park',
    author_email='toracle@gmail.com',
    url='https://github.com/toracle/fab_helper',
    packages=[
        'fab_helper',
    ],
    install_requires=[
        'fabric',
        'fabtools',
        'fabric-virtualenv',
    ],
)
