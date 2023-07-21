import os
import json
import asyncio
from uuid import uuid4
from typing import Any

import redis
import PyPDF2
import aiohttp
import requests

from rabbitmq import RabbitMQThread
import rabbitmq

results = {}


def get_full_path(file_name: str) -> str | None:
    for root, dirs, files in os.walk("/app/aml-dataset"):
        if file_name + ".pdf" in files:
            return os.path.join(root, file_name + ".pdf")


def decode(data: bytes):
    data = data.decode()
    data = data[1:-1].split(', ')
    return data


def callback(ch, method, properties, body, session_id):
    result = json.loads(body)
    results[session_id] = result
    ch.stop_consuming()
    ch.connection.close()


async def old_post(url: str, payload: dict[str, dict]):
    session_id = payload["conf"]["session_id"]

    requests.post(url, json=payload)

    rabbitmq_thread = RabbitMQThread(session_id, callback)
    rabbitmq_thread.start()

    TIMEOUT = 150
    PERIOD = 0.1

    for i in range(int(TIMEOUT / PERIOD)):
        if session_id in results:
            break

        await asyncio.sleep(PERIOD)

    return results[session_id]


async def post(url: str):
    session_id = str(uuid4())

    payload = {
        "conf": {
            "session_id": session_id
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload)) as resp:
            pass


def parse_pdf(pdf_path: str) -> str:
    result = []
    with open(pdf_path, 'rb') as pdf:
        pdf = PyPDF2.PdfReader(pdf_path)
        
        for page in pdf.pages:
            result.extend(page.extract_text().split("\n"))
    
    result = list(filter(lambda x: x != " ", result))
    result = list(map(lambda x: x.strip(), result))
    result = ' '.join(result)
    
    return result


def cache_push(key: Any, value: Any) -> None:
    # Connect to Redis (assuming it's running on localhost and default port)
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    redis_client.set(key, value)


def cache_pull(key: Any) -> Any:
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    
    value = redis_client.get(key)
    if value is not None:
        return value.decode('utf-8')  # Convert from bytes to string if needed
    else:
        return None

