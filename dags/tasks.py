import logging

import pika

logging.basicConfig(level=logging.INFO)


def preprocessing(**context):
    a = 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def another_function(**context):
    kek = 123123123123

    logging.info("Kek: " + str(kek))


def core_nlp(**context):
    a = context["ti"].xcom_pull(key="some_key")
    a += 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def postprocessing(**context):
    a = context["ti"].xcom_pull(key="some_key")
    a += 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)

