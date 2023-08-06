"""Time executions."""
from contextlib import closing
import logging

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from snowflake.connector.pandas_tools import write_pandas

WAREHOUSE = "CPGS"
DATABASE = "FIVETRAN"


def get_run_time_execution_table(
        ds,
        postgres_conn_id,
        snowflake_conn_id,
        table_name,
        rappiflow_instance_name,
        **kwargs,
):
    """
    Connect to airflow database, gets DAG run executions data.

    1. Connect to Airflow Database
    2. Execute SELECT SQL statement on dag_run table
    3. Creates a Pandas DF from results on step 2
    4. Do some transformations
    5. Bulk data to Snowflake rappiflow_dag_executions table

    @return: None
    """
    # Read from Airflow database the DAG run executions times.
    columns = [
        "dag_id",
        "task_id",
        "owners",
        "execution_date",
        "start_date",
        "end_date",
        "state",
    ]

    sql_query = f"""
                  SELECT
                      ti.dag_id,
                      ti.task_id,
                      dag.owners,
                      ti.execution_date,
                      ti.start_date,
                      ti.end_date,
                      ti.state
                  FROM task_instance ti
                  INNER JOIN dag ON ti.dag_id = dag.dag_id
                  WHERE ti.execution_date::date = '{ds}'::date
                  """

    logging.info("Hooking Postgres Connection")
    postgres_hook = PostgresHook(postgres_conn_id=postgres_conn_id)

    logging.info("Getting records from airflow db: %s" % sql_query)
    records = postgres_hook.get_records(sql=sql_query)

    df = pd.DataFrame(records, columns=columns)
    df["rappiflow_name"] = rappiflow_instance_name
    df["run_time_hours"] = df["end_date"] - df["start_date"]
    df["run_time_hours"] = df["run_time_hours"].apply(
        lambda x: "{:.4f}".format(x / pd.Timedelta("1 hour")) if pd.notnull(x) else x
    )

    logging.info("Dataframe Shape: %s" % str(df.shape))

    # When there's not data on end_date, pandas adds a NaT value that brakes the insertion.
    # To avoid it just replace those values with None.
    df = df.astype(str).replace({"NaT": None})

    logging.info("Hooking Snowflake Connection")
    schema = table_name.split('.')[0]
    snowflake_hook = SnowflakeHook(
        snowflake_conn_id=snowflake_conn_id,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=schema
    )

    logging.info("Bulking data into Snowflake")
    with closing(snowflake_hook.get_conn()) as conn:
        cursor = conn.cursor()
        delete_query = f"""
                          DELETE FROM {table_name}
                          WHERE to_date(start_date) = '{ds}'
                          AND RAPPIFLOW_NAME = '{rappiflow_instance_name}'
                          """

        logging.info("Deleting Data: %s" % delete_query)
        cursor.execute(delete_query)
        write_pandas(conn=conn, df=df, table_name=table_name, quote_identifiers=False)
