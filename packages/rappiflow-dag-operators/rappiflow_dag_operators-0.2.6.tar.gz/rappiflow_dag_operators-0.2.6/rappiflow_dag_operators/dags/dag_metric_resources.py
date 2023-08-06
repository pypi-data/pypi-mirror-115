import os

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from rappiflow_dag_operators.operators.utils.time_execution import get_run_time_execution_table
from rappiflow_dag_operators.operators.snowflake_operators import MultiStatementSnowflakeOperator

DAG_ID = "dag_metric_resources"
queries_base_path = os.path.join(os.path.dirname(__file__), 'queries')


def create_dag(
        schedule_interval,
        start_date,
        postgres_conn_id,
        snowflake_conn_id,
        interval,
        catchup,
        dev,
        rappiflow_instance_name
):

    schema = 'cpgs_datascience_dev' if dev else 'cpgs_datascience'
    params = {"rappiflow_name": rappiflow_instance_name,
              "times_execution_table": f"{schema}.rappiflow_dag_executions",
              "prometheus_table": f"{schema}.prometheus_pod_resources",
              "dm_dag_executions": f"{schema}.dm_rappiflow_dag_executions"}

    with DAG(
            dag_id=DAG_ID,
            schedule_interval=schedule_interval,
            max_active_runs=1,
            start_date=start_date,
            catchup=catchup,
            template_searchpath=queries_base_path,
            description="Get DAG metrics resource",
    ) as dag:

        get_dag_times_execution = PythonOperator(
            task_id="get_dag_times_execution",
            python_callable=get_run_time_execution_table,
            provide_context=True,
            op_kwargs={
                "table_name": params['times_execution_table'],
                "rappiflow_instance_name": rappiflow_instance_name,
                "postgres_conn_id": postgres_conn_id,
                "snowflake_conn_id": snowflake_conn_id,
                "interval": interval,
            },
        )

        dm_dag_executions_sql = 'load_daily_dag_executions_information.sql'
        load_daily_dag_executions_information = MultiStatementSnowflakeOperator(
            task_id='load_daily_dag_executions_information',
            sql=dm_dag_executions_sql,
            snowflake_conn_id=snowflake_conn_id,
            params=params
        )

        get_dag_times_execution >> load_daily_dag_executions_information

        return dag
