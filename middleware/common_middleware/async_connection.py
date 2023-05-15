import pika
import common.config as config

def init_rabbit(callback):
    return pika.SelectConnection(
    pika.ConnectionParameters(host=config.RABBIT_HOST), on_open_callback=lambda connection: on_open(connection, callback))

def on_open(connection, callback):
    connection.channel(on_open_callback=callback)

def init_queue(channel, queue_name, exchange_name, callback):
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', callback=lambda frame: on_exchange_declareok(frame, channel, queue_name, exchange_name, callback))

def on_exchange_declareok(frame, channel, queue_name, exchange_name, callback):
    channel.queue_declare(queue_name, callback=lambda frame: on_queue_declareok(frame, channel, queue_name, exchange_name, callback), durable=True)

def on_queue_declareok(frame, channel, queue_name, exchange_name, callback):
    channel.queue_bind(queue_name, exchange_name, callback=lambda frame: on_bindok_trips(frame, channel, queue_name, callback))

def on_bindok_trips(frame, channel, queue_name, callback):
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

def consume_queue(channel, queue_name, callback):
    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback)