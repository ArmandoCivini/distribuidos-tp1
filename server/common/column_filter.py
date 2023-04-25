import logging
import pika
import json

class ColumnFilter:
    def __init__(self):
        self.weather_exchange = 'weather_exchange'
        self.stations_exchange = 'stations_exchange'
        self.trips_exchange = 'trips_exchange'
        #TODO: add variables to configuration
        logging.info('starting pika')#TODO: remove
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.ws_channel = self.init_queue(self.weather_exchange, 'fanout')
        self.ws_channel = self.init_queue(self.stations_exchange, 'fanout')
        self.trips_channel = self.init_queue(self.trips_exchange, 'direct')

    def init_queue(self, exchange, type):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=type)
        return channel
    
    def match_type(self, data):
        columns = []
        exchange = ''
        if data['type'] == 'weather':
            columns = ['type', 'city', 'date', 'prectot'] #TODO: add to configuration
            exchange = self.weather_exchange
        elif data['type'] == 'stations':
            columns = ['type', 'city', 'code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
            exchange = self.stations_exchange
        elif data['type'] == 'trips':
            columns = ['city', 'start_date', 'start_station_code', 'end_station_code', 'duration_sec'] #TODO: add to configuration
            exchange = self.trips_exchange
        else:
            logging.error('unknown type: %s', data['type'])
            return None, None
        return columns, exchange
    
    def filter(self, data):
        columns, exchange = self.match_type(data)
        if not columns:
            return
        filtered_data = self.filter_columns(data, columns)
        self.ws_channel.basic_publish(
        exchange=exchange,
        routing_key='',
        body=json.dumps(filtered_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
        return
    
    #TODO: destroy function

    def filter_columns(self, data, columns):
        filtered_data = {}
        for column in columns:
            filtered_data[column] = data[column]
        return filtered_data



    def __del__(self):
        try:
            logging.info('closing rabbitmq connection')
            # self.connection.close()
        except:
            pass
        return