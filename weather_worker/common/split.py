import pika
import logging
import json

class Split:
    def __init__(self, trips_queue):
        #TODO: add to configuration
        self.trips_exchange = 'trips_exchange'
        self.trips_queue = trips_queue
        self.notif_exchange = 'notif_exchange'
        self.notif_queue = ''
        self.trip_count = 0
        self.connection = pika.SelectConnection(
    pika.ConnectionParameters(host='rabbitmq'), on_open_callback=self.on_open)
        
    def on_open(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.basic_qos(prefetch_count=1)
        # channel.queue_declare(queue=self.trips_queue)
        channel.exchange_declare(callback=self.on_exchange_declareok_trips, exchange=self.trips_exchange, exchange_type='fanout')
        channel.exchange_declare(callback=self.on_exchange_declareok_notif, exchange=self.notif_exchange, exchange_type='fanout')

        # channel.basic_consume(queue=self.trips_queue, on_message_callback=self.callback_trips)

    def on_exchange_declareok_notif(self, frame):
        self.channel.queue_declare(self.notif_queue, callback=self.on_queue_declareok_notif)
    
    def on_exchange_declareok_trips(self, frame):
        self.channel.queue_declare(self.trips_queue, callback=self.on_queue_declareok_trips)

    def on_queue_declareok_notif(self, frame):
        self.channel.queue_bind(self.notif_queue, self.notif_exchange, callback=self.on_bindok_notif)

    def on_queue_declareok_trips(self, frame):
        self.channel.queue_bind(self.trips_queue, self.trips_exchange, callback=self.on_bindok_trips)

    def on_bindok_notif(self, frame):
        self.channel.basic_consume(queue=self.notif_queue, on_message_callback=self.callback_notif)

    def on_bindok_trips(self, frame):
        self.channel.basic_consume(queue=self.trips_queue, on_message_callback=self.callback_trips)

    def split(self):
        # ended_stations.wait() #wait for stations to be ready
        try:
            self.connection.ioloop.start()
        except:
            logging.info('error receiving trips')
            self.connection.close()
            return
        logging.info(f'finished consuming trips: {self.trip_count}')
        self.connection.close()

    def callback_notif(self, ch, method, properties, body):
        if body.decode("utf-8")  == 'end trips':
            logging.info('received end for trips')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.ioloop.stop()
            return
        logging.info("Received notif {}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_trips(self, ch, method, properties, body):
        logging.info("Received trip {}".format(body))
        self.trip_count += 1
        try:
            trip = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)



   