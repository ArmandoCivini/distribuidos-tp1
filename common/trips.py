import pika
import logging
import json
import random

def split_trips(trips):
    city = trips.pop("city")
    trip_list = []
    for i in range(len(trips['start_date'])):
        trip_values = {}
        for column in trips:
            trip_values[column] = trips[column][i]
        trip_values['city'] = city
        trip_list.append(trip_values)
    return trip_list

class Trips:
    def __init__(self, trips_queue, process_callback, result):
        self.process_callback = process_callback
        self.result = result
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

        channel.exchange_declare(callback=self.on_exchange_declareok_trips, exchange=self.trips_exchange, exchange_type='fanout')
        channel.exchange_declare(callback=self.on_exchange_declareok_notif, exchange=self.notif_exchange, exchange_type='fanout')

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

    def trips(self, data):
        self.data = data
        try:
            self.connection.ioloop.start()
        except:
            logging.info('error receiving trips')
            self.connection.close()
            return
        logging.info(f'finished consuming trips')
        self.connection.close()
        logging.info(f'MARCELO: {self.trip_count}')
        return self.result

    def callback_notif(self, ch, method, properties, body):
        if body.decode("utf-8")  == 'end trips':
            logging.info('received end for trips')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.ioloop.stop()
            return
        logging.info("Received notif {}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_trips(self, ch, method, properties, body):
        try:
            trip = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        trip_list = split_trips(trip)
        for trip in trip_list:
            if random.randint(0, 50000) < 1: logging.info(f"processing trip: {trip}")
            self.trip_count += 1
            try:
                result = self.process_callback(trip, self.data, self.result)
                self.result = result
            except Exception as e:
                logging.error(f"failed to process trip: {trip}, with exception: {e}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
        ch.basic_ack(delivery_tag=method.delivery_tag)



   