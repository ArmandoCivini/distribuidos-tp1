from common.stations import Stations
from common.trips import Trips
import multiprocessing as mp
from common.process_station import process_trips_stations
import logging

class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.manager = mp.Manager()
        self.ended_stations = self.manager.Event()
        self.trips = Trips('trips_stations_queue')
        self.stations = Stations(consumer_id, self.ended_stations)

    def run(self):
        stations_montreal, stations_wt = self.stations.get_stations()
        result = {'year_count':{}, 'total_distance': {}}
        result = self.trips.trips([stations_montreal, stations_wt], process_trips_stations, result)
        logging.info('result: {}'.format(result))
