#!/usr/bin/env python3
import pika
import time
import os
import logging

def main():
    # Wait for rabbitmq to come up
    logging.info('started worker')
    time.sleep(10)
    logging.info('finished sleep')
    consumer_id = os.environ["WORKER_ID"]
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))

    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    logging.info('[{}] Waiting for messages. To exit press CTRL+C'.format(consumer_id))


    def callback(ch, method, properties, body):
        logging.info("[{}] Received {}".format(consumer_id, body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()

if __name__ == "__main__":
    main()