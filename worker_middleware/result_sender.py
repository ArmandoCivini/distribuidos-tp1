import pika
import json

def send_results(results, queue):
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(
    exchange='',
    routing_key=queue,
    body=json.dumps(results),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))
    connection.close()



   