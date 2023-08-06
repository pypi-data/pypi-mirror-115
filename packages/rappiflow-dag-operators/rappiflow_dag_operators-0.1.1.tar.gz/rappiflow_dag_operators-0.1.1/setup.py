#!/usr/bin/env python

from setuptools import setup

with open("rappiflow_dag_operators.egg-info/requires.txt") as f:
    required = f.read().splitlines()

setup(
    name='rappiflow_dag_operators',
    version='0.1.1',
    author='cpgs-ds-eng',
    author_email='eduardocarhue@gmail.com',
    description='Rappiflow Dags and Operators utils',
    install_requires=required,
)
