import logging
import pika
import json

class ColumnFilter:
    def __init__(self):
        self.weather_exchange = 'weather_exchange'
        self.stations_exchange = 'stations_exchange'
        self.trips_exchange = ''
        self.trips_queue = 'trips_queue'
        #TODO: add variables to configuration
        logging.info('starting pika')#TODO: remove
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()
        self.init_queue(self.weather_exchange, 'fanout')
        self.init_queue(self.stations_exchange, 'fanout')
        self.init_queue_trips(self.trips_queue)
        
    def init_queue_trips(self, queue):
        self.channel.queue_declare(queue=queue, durable=True)

    def init_queue(self, exchange, type):
        self.channel.exchange_declare(exchange=exchange, exchange_type=type)
    
    def match_type(self, data):
        columns = []
        exchange = ''
        channel = self.channel
        routing_key = ''
        if data['type'] == 'weather':
            columns = ['city', 'date', 'prectot'] #TODO: add to configuration
            exchange = self.weather_exchange
        elif data['type'] == 'stations':
            columns = ['city', 'code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
            exchange = self.stations_exchange
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
    
    #TODO: destroy function

    def filter_columns(self, data, columns):
        filtered_data = {}
        for column in columns:
            filtered_data[column] = data[column]
        return filtered_data
    
    def send_end_stations(self):
        self.channel.basic_publish(
        exchange=self.stations_exchange,
        routing_key='',
        body='end',
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ))


    def __del__(self):
        try:
            logging.info('closing rabbitmq connection')
            #self.connection.close()
        except:
            pass
        return