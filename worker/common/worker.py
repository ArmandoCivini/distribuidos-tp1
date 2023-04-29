from common.stations import Stations
from common.split import Split
import multiprocessing as mp


class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.manager = mp.Manager()
        self.ended_stations = self.manager.Event()
        self.stations = Stations(consumer_id, self.ended_stations)
        self.split = Split('trips_stations_queue')

    def run(self):
        # self.stations_process = mp.Process(target=self.stations.run(), args=())
        # self.stations_process.start()
        self.split.split(self.ended_stations, self.consumer_id)
        # self.stations_process.join()
