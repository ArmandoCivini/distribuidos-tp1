import logging
import pika
import time
import json

class ColumnFilter:
    def __init__(self):
        time.sleep(10) #TODO: remove
        logging.info('starting pika')#TODO: remove
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)
        #TODO: add variables to configuration

    def filter(self, data):
        self.channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    #TODO: destroy function