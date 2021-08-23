import uuid
import pika
import datetime

from . import socketio
from chatapp.db import get_db


class BotHandler(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result_queue = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result_queue.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, stock_code):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='stock_bot_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(stock_code))
        while self.response is None:
            self.connection.process_data_events()
        self.response = self.response.decode('utf-8')
        return self.response


def handle_bot_message(stock_code):
    bh = BotHandler()
    response = bh.call(stock_code)
    dt = datetime.datetime.now().strftime('%m-%d-%Y %H:%M')
    return response


