#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from setuptools import setup
from setuptools import find_packages

REQUIREMENTS = [
    'requests==2.21.0',
    'stevedore==1.29.0',
    'six',  # Do not specify version: the last version of setuptools require six>=1.10.0
]

setup(
    name='wazo_lib_rest_client',
    version='0.2',

    description='a simple library to instantiate REST clients',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),
    install_requires=REQUIREMENTS,

    entry_points={
        'test_rest_client.commands': [
            'example = wazo_lib_rest_client.example_cmd:ExampleCommand',
        ],
    }
)
