from threading import Thread
from functools import partial

import pika


class RabbitMQThread(Thread):
    def __init__(self, queue_name, callback):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'),
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

        partial_callback = partial(callback, session_id=queue_name)

        self.consumer = self.channel.basic_consume(
            queue=queue_name, 
            on_message_callback=partial_callback, 
            auto_ack=True,
        )

    def run(self):
        self.channel.start_consuming()

