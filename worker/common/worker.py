from common.stations import Stations
from common.split import split
import multiprocessing as mp


class Worker:
    def __init__(self, consumer_id):
        self.consumer_id = consumer_id
        self.manager = mp.Manager()
        self.ended_stations = self.manager.Event()
        self.stations = Stations(consumer_id, self.ended_stations)

    def run(self):
        self.stations_process = mp.Process(target=self.stations.run(), args=())
        self.stations_process.start()
        split(self.ended_stations)
        self.stations_process.join()
