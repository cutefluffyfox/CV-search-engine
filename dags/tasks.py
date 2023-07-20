#!/usr/local/bin/python3

import pika
import json
import logging
from threading import Thread

from vectorizer import Vector
from sorter import CVSorter


import preprocessing
# from dags import preprocessing

logging.basicConfig(level=logging.INFO)

PDFS_FOLDER_PATH = "/app/aml-dataset"


def preprocessing_task_1(**context):
    prompt = context['params']['prompt']

    pdfs_path = preprocessing.find(PDFS_FOLDER_PATH)

    pdfs_path = filter(lambda path: "HR" in path, pdfs_path)  
    # TODO: remove it asap

    pdfs_path = list(pdfs_path)
    
    pdfs_ids = list(map(lambda path: path.split('/')[-1].split('.')[0], pdfs_path))

    logging.info(f"pdfs path: " + str(pdfs_path))

    result = []

    for pdf_path in pdfs_path:
        pdf = preprocessing.parse_pdf(pdf_path)
        pdf = preprocessing.preprocess(pdf)

        result.append(pdf)

    payload = []

    for i in range(len(result)):
        payload.append({"id": pdfs_ids[i], "text": result[i]})

    context["ti"].xcom_push(key="prompt", value=prompt)
    context["ti"].xcom_push(key="cvs", value=payload)


def vectorization(**context):
    prompt: str = context['ti'].xcom_pull(key='prompt')
    cvs: list[dict] = context['ti'].xcom_pull(key="cvs")  # list[dict{id, text}]

    prompt_vec_list = [None]
    
    def kek(prompt_vec_list):
        prompt_vec = Vector(-1, prompt).to_dict()
        prompt_vec_list[0] = prompt_vec

    thread = Thread(target=kek, args=(prompt_vec_list,))
    thread.start()
    thread.join()

    prompt_vec = prompt_vec_list[0]

    cv_vecs = [None]

    def lol(cv_vecs_list, cvs):
        cv_vecs_list[0] = [Vector(cv['id'], cv['text']).to_dict() for cv in cvs]

    thread_2 = Thread(target=lol, args=(cv_vecs, cvs))
    thread_2.start()
    thread_2.join()

    cv_vecs = cv_vecs[0]

    print("Cv vecs: " + str(cv_vecs))

    context['ti'].xcom_push(key='prompt_vec', value=prompt_vec)
    context['ti'].xcom_push(key='cv_vecs', value=cv_vecs)


def sorting(**context):
    def thread_function(prompt_vec_list: list, cv_vecs_list: list) -> None:
        prompt_vec_list[0] = Vector.from_dict(**context['ti'].xcom_pull(key='prompt_vec'))
        cv_vecs_list[0] = Vector.parse_iterative(context['ti'].xcom_pull(key='cv_vecs'))

    prompt_vec = [None]
    cv_vecs = [None]

    thread = Thread(target=thread_function, args=(prompt_vec, cv_vecs))
    thread.start()
    thread.join()

    prompt_vec: Vector = prompt_vec[0]
    cv_vecs: list[Vector] = cv_vecs[0]

    print("Prompt_vec: " + str(prompt_vec))
    print("Cv_vecs: " + str(cv_vecs))

    sorter = CVSorter(prompt_vec, cv_vecs)
    metadata = sorter.get_sorted_metadata()

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    session_id = context['params']['session_id']

    channel.queue_declare(queue=session_id)

    channel.basic_publish(
        exchange='',
        routing_key=session_id,
        body=json.dumps(metadata),
    )

    connection.close()

    # context['ti'].xcom_puch(key='cvs', value=metadata)
