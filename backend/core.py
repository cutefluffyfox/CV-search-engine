import os
import json
import asyncio
from uuid import uuid4

import requests
import aiohttp

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


async def old_post(url: str, prompt: str):
    session_id = str(uuid4())

    payload = {
        "conf": {
            "session_id": session_id,
            "prompt": prompt
        }
    }

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

