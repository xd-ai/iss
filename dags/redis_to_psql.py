from airflow.models import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

from cron import update_psql

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 3, 4),
}

with DAG(
        dag_id='redis_to_psql',
        default_args=default_args,
        schedule_interval="* * * * *"
) as dag:
    to_psql_task = PythonOperator(task_id='write_minute_data',
                                  python_callable=update_psql)
