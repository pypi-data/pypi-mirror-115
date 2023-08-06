#!/usr/bin/env python

from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='rappiflow_dag_operators',
    version='0.2.0',
    author='cpgs-ds-eng',
    author_email='eduardocarhue@gmail.com',
    description='Rappiflow Dags and Operators utils',
    install_requires=required,
)
