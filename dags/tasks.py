import logging
import pandas as pd
from random import random
import pika

logging.basicConfig(level=logging.INFO)


def preprocessing(**context):
    a = 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def core_nlp(**context):
    a = context["ti"].xcom_pull(key="some_key")

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def postprocessing(**context):
    logging.info('Started score calculation')
    df = pd.read_csv('data/Resume/Resume.csv')
    ids = [{'id': rid, 'score': random()} for rid in df['ID'].to_list()]
    ids.sort(key=lambda r: r['score'], reverse=True)
    context["ti"].xcom_push(key="cvs", value=ids)

