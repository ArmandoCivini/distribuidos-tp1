from common.stations import Stations
from common.result_sender import send_results
from common_extra.trips import Trips
from common.process_station import process_trips_stations
import logging

class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        result = {'year_count':{}, 'total_distance': {}}
        self.trips = Trips('trips_stations_queue', process_trips_stations, result)
        self.stations = Stations(consumer_id)

    def run(self):
        stations_montreal, stations_toronto, stations_washington = self.stations.get_stations()
        result = self.trips.trips([stations_montreal, stations_toronto, stations_washington])
        logging.info('result: {}'.format(result))
        send_results(result, 'stations_result_queue')#TODO: add to configuration

