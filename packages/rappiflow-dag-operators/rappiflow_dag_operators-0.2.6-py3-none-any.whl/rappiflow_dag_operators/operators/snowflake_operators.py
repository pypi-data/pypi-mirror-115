"""Snowflake Operators.

There is an existing snowflake_operator.py included with Airflow code. We are extending that module to support
features Snowflake does not include at the moment.
"""
from typing import Optional
from contextlib import closing

from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class MultiStatementSnowflakeOperator(BaseOperator):
    """Executes multiple sql statements.

    This Operator uses the `conn.execute_string` method of Snowflake Connector that allows running multiple sql
    statements.
    """

    template_fields = ('sql',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, sql: str, snowflake_conn_id: str = 'snowflake_default', parameters: Optional[dict] = None,
                 warehouse: Optional[str] = None, database: Optional[str] = None, *args, **kwargs):
        """Class Initializer.

        :param sql: the str of sql code to be executed. (templated)
        :type sql: A str representing a sql statement, or reference to a template file.
            Template reference are recognized by str ending in '.sql'
        :param parameters: extra information to process the queries
        :type parameters: dict
        :param snowflake_conn_id: reference to specific snowflake connection id
        :type snowflake_conn_id: str
        :param warehouse: name of warehouse which overwrite defined one in connection
        :type warehouse: str
        :param database: name of database which overwrite defined one in connection
        :type database: str
        """
        super().__init__(*args, **kwargs)
        self.snowflake_conn_id = snowflake_conn_id
        self.sql = sql
        self.parameters = parameters
        self.warehouse = warehouse
        self.database = database

    def get_hook(self) -> SnowflakeHook:
        """Get Hook."""
        return SnowflakeHook(
            snowflake_conn_id=self.snowflake_conn_id,
            warehouse=self.warehouse,
            database=self.database
        )

    def execute(self, context: dict) -> None:
        """Execute Multi Statement SQLs inside a Transaction."""
        self.log.info('Executing: %s', self.sql)

        with closing(self.get_hook().get_conn()) as conn:
            conn.execute_string(self.sql, params=self.parameters)
