from common.stations import Stations
from common_extra.trips import Trips
import multiprocessing as mp
from common.process_station import process_trips_stations
import logging

class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.manager = mp.Manager()
        self.ended_stations = self.manager.Event()
        result = {'year_count':{}, 'total_distance': {}}
        self.trips = Trips('trips_stations_queue', process_trips_stations, result)
        self.stations = Stations(consumer_id, self.ended_stations)

    def run(self):
        stations_montreal, stations_wt = self.stations.get_stations()
        logging.info('stations_montreal: {}'.format(stations_montreal))
        result = self.trips.trips([stations_montreal, stations_wt])
        logging.info('result: {}'.format(result))
