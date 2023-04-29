import logging
import pika
import json
import random #TODO: remove

class Stations:
    def __init__(self, consumer_id, ended_stations):
        self.stations_exchange = 'stations_exchange'
        self.stations_queue = ''
        self.consumer_id = consumer_id
        self.keys = ['code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
        self.stations_montreal = self.add_keys(self.keys)
        self.stations_wt = self.add_keys(self.keys)
        self.ended_stations = ended_stations

    def add_keys(self, keys):
        _dict = {}
        for key in keys:
            _dict[key] = []
        return _dict

    def run(self):
        self.get_stations()

    def get_stations(self):
        stations_exchange = self.stations_exchange
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()

        channel.exchange_declare(exchange=stations_exchange, exchange_type='fanout')

        result = channel.queue_declare(queue=self.stations_queue)
        queue_name = result.method.queue

        channel.queue_bind(exchange=stations_exchange, queue=queue_name)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, properties, body: self.callback(ch, method, body))

        channel.start_consuming()
        logging.info(f"finished consuming stations: {len(self.stations_montreal['code']) + len(self.stations_wt['code'])}")

    def callback(self, ch, method, body):
        if body.decode("utf-8")  == 'end':
            logging.info('received end for stations')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.ended_stations.set() #tell split that all stations are ready
            ch.stop_consuming()
            return
        # if random.randint(0, 100) < 10:
        #     logging.info("[{}] Received {}".format(self.consumer_id, body))
        try:
            station = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        for column in self.keys:
            if station['city'] == 'montreal':
                self.stations_montreal[column].append(station[column])
            else:
                self.stations_wt[column].append(station[column])
        ch.basic_ack(delivery_tag=method.delivery_tag)