from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from tasks import *


with DAG(
    dag_id='second_sample_dag',
    start_date=datetime(2022, 5, 28),
    schedule_interval=None
) as dag:
    interpret_text = PythonOperator(
        task_id="interpretation",
        python_callable=interpret_text_callback
    )

    push_to_rabbit = PythonOperator(
        task_id="pushing",
        python_callable=push_to_rabbit
    )

interpret_text >> push_to_rabbit

