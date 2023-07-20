from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from tasks import *

with DAG(
    dag_id='first_sample_dag',
    start_date=datetime(2022, 5, 28),
    schedule_interval=None
) as dag:
    preprocessing_task = PythonOperator(
        task_id='preprocessing_task',
        python_callable=preprocessing_task_1
    )

    nlp_vectorization_task = PythonOperator(
        task_id='nlp_vectorization',
        python_callable=vectorization,
    )

    sorting_task = PythonOperator(
        task_id='sorting',
        python_callable=sorting
    )

preprocessing_task >> nlp_vectorization_task >> sorting_task

