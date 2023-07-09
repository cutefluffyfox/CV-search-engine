from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from tasks import *

with DAG(
    dag_id='first_sample_dag',
    start_date=datetime(2022, 5, 28),
    schedule_interval=None
) as dag:
    preprocessing_task = PythonOperator(
        task_id='preprocessing_task',
        python_callable=preprocessing
    )

    nlp_vectorization_task = PythonOperator(
        task_id='nlp_vectorization',
        python_callable=nlp_vectorization_task
    )

    core_nlp_task = PythonOperator(
        task_id='core_nlp',
        python_callable=core_nlp
    )

    postprocessing_task = PythonOperator(
        task_id='postprocessing',
        python_callable=postprocessing
    )

preprocessing_task >> nlp_vectorization_task >> core_nlp_task >> postprocessing_task

