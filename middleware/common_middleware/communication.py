import pika
import common.config as config

def init_connection(exchanges):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.RABBIT_HOST))
    channel = connection.channel()
    for exchange in exchanges:
        channel.exchange_declare(exchange=exchange, exchange_type='fanout', auto_delete=False)
    return connection, channel

def init_exchange(channel, exchange, queues):
    channel.exchange_declare(exchange=exchange, exchange_type='fanout', auto_delete=False)
    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)

def publish_message(channel, exchange, routing_key, message):
    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        )
    )