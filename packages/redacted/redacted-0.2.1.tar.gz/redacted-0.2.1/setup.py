#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


with open('requirements/test.txt') as f:
    test_requirements = f.read().splitlines()


setup(
    author='Mitchell Lisle',
    author_email='m.lisle90@gmail.com',
    description='📛 An experimental data anonymisation library',
    install_requires=requirements,
    include_package_data=True,
    keywords='redacted',
    name='redacted',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mitchelllisle/redacted',
    version='0.2.1',
    zip_safe=False,
)
