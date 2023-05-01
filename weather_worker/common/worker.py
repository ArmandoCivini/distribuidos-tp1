from common.weather import Weather
from common_extra.result_sender import send_results
from common_extra.trips import Trips
from common.process_weather import process_trips_weather
import logging

class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        result = {'duration': 0, 'count': 0}
        self.trips = Trips('trips_weather_queue', process_trips_weather, result)
        self.weather = Weather(consumer_id)

    def run(self):
        weather_montreal, weather_toronto, weather_washington = self.weather.get_weather()
        result = self.trips.trips([weather_montreal, weather_toronto, weather_washington])
        logging.info('result: {}'.format(result))
        send_results(result, 'weather_result_queue')#TODO: add to configuration