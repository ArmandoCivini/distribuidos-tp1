import logging
import pika
import json
from time import sleep

class ColumnFilter:
    def __init__(self):
        self.consumer_num = 2
        self.weather_exchange = 'weather_exchange'
        self.stations_exchange = 'stations_exchange'
        self.notif_exchange = 'notif_exchange'
        self.trips_exchange = 'trips_exchange'
        self.weather_queue = ''
        self.stations_queue = ''
        self.notif_queue = ''
        self.trips_queue = ''
        self.trips_weather_queue = 'trips_weather_queue'
        self.trips_stations_queue = 'trips_stations_queue'
        #TODO: add variables to configuration
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.init_queue(self.weather_exchange, 'fanout')
        self.init_queue(self.stations_exchange, 'fanout')
        self.init_queue(self.notif_exchange, 'fanout')
        self.init_queue_trips([self.trips_stations_queue, self.trips_weather_queue])
        
    def init_queue_trips(self, queues):
        self.init_queue(self.trips_exchange, 'fanout')
        for queue in queues:
            self.channel.queue_declare(queue=queue)

    def init_queue(self, exchange, type):
        self.channel.exchange_declare(exchange=exchange, exchange_type=type, auto_delete=False)
    
    def match_type(self, data):
        columns = []
        exchange = ''
        channel = self.channel
        routing_key = ''
        if data['type'] == 'weather':
            columns = ['city', 'date', 'prectot'] #TODO: add to configuration
            exchange = self.weather_exchange
            routing_key = self.weather_queue
        elif data['type'] == 'stations':
            columns = ['city', 'code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
            exchange = self.stations_exchange
            routing_key = self.stations_queue
        elif data['type'] == 'trips':
            columns = ['city', 'start_date', 'start_station_code', 'end_station_code', 'duration_sec'] #TODO: add to configuration
            exchange = self.trips_exchange
            routing_key = self.trips_queue
        else:
            logging.error('unknown type: %s', data['type'])
            return None, None
        return columns, exchange, channel, routing_key
    
    def filter(self, data):
        columns, exchange, channel, routing_key = self.match_type(data)
        if not columns:
            return
        filtered_data = self.filter_columns(data, columns)
        channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=json.dumps(filtered_data),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ))
        return

    def filter_columns(self, data, columns):
        filtered_data = {}
        for column in columns:
            filtered_data[column] = data[column]
        return filtered_data
    
    def send_end(self, channel, exchange, routing_key):
        channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body='end',
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ))
    
    def send_end_stations(self):
        self.send_end(self.channel, self.stations_exchange, self.stations_queue)
    
    def send_end_weather(self):
        self.send_end(self.channel, self.weather_exchange, self.weather_queue)
    
    def send_end_trips(self):
        logging.info(f'sending end trips')
        while True:
            stations_result = self.channel.queue_declare(queue=self.trips_stations_queue, passive=True)
            weather_result = self.channel.queue_declare(queue=self.trips_weather_queue, passive=True)
            if stations_result.method.message_count == 0 and weather_result.method.message_count == 0:
                logging.info(f'queue is empty, sending')
                self.channel.basic_publish(
                exchange=self.notif_exchange,
                routing_key=self.notif_queue,
                body='end trips',
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                ))
                return
            else:
                logging.info(f'queue has messages, waiting')
                sleep(1)


    def close(self):
        try:
            self.send_end_stations()
            self.send_end_weather()
            self.send_end_trips()
            logging.info('closing rabbitmq connection')
            self.connection.close()
        except:
            pass
        return