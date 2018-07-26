#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import py3dtiles_batcher

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='py3dtiles_batcher',
    version=py3dtiles_batcher.__version__,
    description="Create 3dtiles tileset.json with py3dtiles in batch.",
    long_description=long_description,
    author="Loïc Messal",
    author_email='Tofull@users.noreply.github.com',
    url='https://github.com/tofull/py3dtiles_batcher',
    packages=find_packages(include=['py3dtiles_batcher']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': ['py3dtiles_batcher=py3dtiles_batcher.command_line:command_line'],
    }
)