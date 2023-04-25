import logging
import pika
import json

class Stations:
    def __init__(self, consumer_id):
        self.stations_exchange = 'stations_exchange'
        self.consumer_id = consumer_id
        self.stations = {}

    def run(self):
        self.get_stations()

    def get_stations(self):
        stations_exchange = self.stations_exchange
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        channel.exchange_declare(exchange=stations_exchange, exchange_type='fanout') #TODO: add variables to configuration

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=stations_exchange, queue=queue_name)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, properties, body: self.callback(ch, method, body))

        channel.start_consuming()
        logging.info("finished consuming")

    def callback(self, ch, method, body):
        logging.info("[{}] Received {}".format(self.consumer_id, body))
        station = json.loads(body)
        for column in station.keys():
            if column not in self.stations:
                self.stations[column] = []
            self.stations[column].append(station[column])
        ch.basic_ack(delivery_tag=method.delivery_tag)