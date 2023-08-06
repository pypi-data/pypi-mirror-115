"""rappiflow_dag_operators module."""
from pkg_resources import get_distribution, DistributionNotFound
from rappiflow_dag_operators.dags.dag_metric_resources import create_dag
from rappiflow_dag_operators.dags.test_class import TestPackage

LIB_NAME = "rappiflow_dag_operators"

try:
    _dist = get_distribution(LIB_NAME)
except DistributionNotFound:
    __version__ = f"Please install {LIB_NAME} project"
else:
    __version__ = _dist.version

__all__ = ["create_dag", "TestPackage"]
