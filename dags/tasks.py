import logging

from vectorizer import Vector
from sorter import CVSorter


logging.basicConfig(level=logging.INFO)


def preprocessing(**context):
    a = 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def vectorization(**context):
    prompt: str = context['ti'].xcom_pull(key='prompt')
    cvs: list[dict] = context['ti'].xcom_pull(key="cvs")  # list[dict{id, text}]

    prompt_vec = Vector(-1, prompt)
    cv_vecs = [Vector(cv['id'], cv['text']) for cv in cvs]

    context['ti'].xcom_push(key='prompt_vec', value=prompt_vec)
    context['ti'].xcom_puch(key='cv_vecs', value=cv_vecs)


def sorting(**context):
    prompt_vec: Vector = context['ti'].xcom_pull(key='prompt_vec')
    cv_vecs: list[Vector] = context['ti'].xcom_pull(key='cv_vecs')

    sorter = CVSorter(prompt_vec, cv_vecs)
    metadata = sorter.get_sorted_metadata()

    context['ti'].xcom_puch(key='cvs', value=metadata)
