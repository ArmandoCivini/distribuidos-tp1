import logging
import pika
import time
import json

class ColumnFilter:
    def __init__(self):
        self.weather_stations_exchange = 'weather_stations_queue'
        self.trips_exchange = 'trips_queue'
        #TODO: add variables to configuration
        logging.info('starting pika')#TODO: remove
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.ws_channel = self.init_queue(self.weather_stations_exchange, 'fanout')
        self.trips_channel = self.init_queue(self.trips_exchange, 'direct')

    def init_queue(self, exchange, type):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=type)
        return channel

    def filter(self, data):
        if data['type'] == 'weather' or data['type'] == 'stations':
            self.filter_weather_or_stations(data)
        elif data['type'] == 'trips':
            self.filter_trips(data)
        else:
            logging.error('unknown type: %s', data['type'])
            return
        return
    #TODO: destroy function

    def filter_columns(self, data, columns):
        filtered_data = {}
        for column in columns:
            filtered_data[column] = data[column]
        return filtered_data

    def filter_weather_or_stations(self, data):
        columns = []
        if data['type'] == 'weather':
            columns = ['type', 'city', 'date', 'prectot'] #TODO: add to configuration
        else:
            columns = ['type', 'city', 'code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
        filtered_data = self.filter_columns(data, columns)
        self.ws_channel.basic_publish(
        exchange=self.weather_stations_exchange,
        routing_key='',
        body=json.dumps(filtered_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))

    def filter_trips(self, data):
        columns = ['city', 'start_date', 'start_station_code', 'end_station_code', 'duration_sec'] #TODO: add to configuration
        filtered_data = self.filter_columns(data, columns)
        self.trips_channel.basic_publish(
        exchange=self.trips_exchange,
        routing_key='',
        body=json.dumps(filtered_data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))

    def __del__(self):
        try:
            logging.info('closing rabbitmq connection')
            # self.connection.close()
        except:
            pass
        return