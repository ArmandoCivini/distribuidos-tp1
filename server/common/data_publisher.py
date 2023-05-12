import logging
import json
from common_middleware.communication import publish_message, init_connection, init_exchange
from common.filter import filter_data
import common.config as config

class DataPublisher:
    def __init__(self):
        self.weather_exchange = config.WEATHER_EXCHANGE
        self.stations_exchange = config.STATIONS_EXCHANGE
        self.notif_exchange = config.NOTIF_EXCHANGE
        self.trips_exchange = config.TRIPS_EXCHANGE
        self.weather_queue = config.WEATHER_QUEUE
        self.stations_queue = config.STATIONS_QUEUE
        self.notif_queue = config.NOTIF_QUEUE
        self.trips_queue = config.TRIPS_QUEUE
        self.trips_weather_queue = config.TRIPS_WEATHER_QUEUE
        self.trips_stations_queue = config.TRIPS_STATIONS_QUEUE
        self.connection, self.channel = init_connection([self.weather_exchange, self.stations_exchange, self.notif_exchange])
        init_exchange(self.channel, self.trips_exchange, [self.trips_stations_queue, self.trips_weather_queue])
    
    def match_type(self, data):
        exchange = ''
        channel = self.channel
        routing_key = ''
        if data['type'] == config.WEATHER_TYPE:
            exchange = self.weather_exchange
            routing_key = self.weather_queue
        elif data['type'] == config.STATIONS_TYPE:
            exchange = self.stations_exchange
            routing_key = self.stations_queue
        elif data['type'] == config.TRIPS_TYPE:
            exchange = self.trips_exchange
            routing_key = self.trips_queue
        else:
            logging.error('unknown type: %s', data['type'])
            return None, None, None, None
        filtered_data = filter_data(data)
        return filtered_data, exchange, channel, routing_key
    
    def publish(self, data):
        filtered_data, exchange, channel, routing_key = self.match_type(data)
        if not filtered_data:
            return
        publish_message(channel, exchange, routing_key, json.dumps(filtered_data))
        return
    
    def send_end(self, channel, exchange, routing_key):
        publish_message(channel, exchange, routing_key, config.END_MESSAGE)
    
    def send_end_stations(self):
        self.send_end(self.channel, self.stations_exchange, self.stations_queue)
    
    def send_end_weather(self):
        self.send_end(self.channel, self.weather_exchange, self.weather_queue)
    
    def send_end_trips(self):
        logging.info(f'sending end trips')
        publish_message(self.channel, self.notif_exchange, self.notif_queue, config.END_TRIPS_MESSAGE)

    def close(self):
        try:
            logging.info('closing rabbitmq connection')
            self.connection.close()
        except:
            pass
        return