import logging
import json
import random
import common.config as config
from common_middleware.async_connection import init_rabbit, init_queue

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
        self.trips_exchange = config.TRIPS_EXCHANGE
        self.trips_queue = trips_queue
        self.notif_exchange = config.NOTIF_EXCHANGE
        self.notif_queue = config.NOTIF_QUEUE
        self.trip_count = 0
        self.finished = False
        self.connection = init_rabbit(self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.basic_qos(prefetch_count=1)
        
        init_queue(channel, self.trips_queue, self.trips_exchange, self.callback_trips)
        init_queue(channel, self.notif_queue, self.notif_exchange, self.callback_notif)

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
        logging.info(f'trip count: {self.trip_count}')
        return self.result

    def callback_notif(self, ch, method, properties, body):
        if body.decode("utf-8")  == config.END_TRIPS_MESSAGE:
            logging.info('received end for trips')
            self.finished = True
        else:
            logging.info("Received notif {}".format(body))
        self.check_end()
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def callback_trip(self, trip):
        try:
            result = self.process_callback(trip, self.data, self.result)
            self.result = result
        except Exception as e:
            return
        
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
            self.callback_trip(trip)
        self.check_end()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def check_end(self):
        self.channel.queue_declare(callback=self.queue_declare_pasive_callback, queue=self.trips_queue, passive=True)
    
    def queue_declare_pasive_callback(self, method_frame):
        if self.finished and method_frame.method.message_count == 0:
            self.connection.ioloop.stop()
    
    def graceful_shutdown(self):
        try:
            self.connection.ioloop.stop()
            self.connection.close()
        except:
            pass


   