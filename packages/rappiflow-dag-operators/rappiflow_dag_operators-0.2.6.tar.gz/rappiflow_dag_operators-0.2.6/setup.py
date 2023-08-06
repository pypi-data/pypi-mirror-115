import os
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="rappiflow_dag_operators",
    version="0.2.6",
    author="CPGS DS Team",
    description='Rappiflow Dags and Operators utils',
    install_requires=requirements,
    packages=find_packages(),
    python_requires=">=3.7",
)
