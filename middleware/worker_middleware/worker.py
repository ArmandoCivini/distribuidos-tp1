from common_middleware.result_sender import send_results
from middleware.trips import Trips
import logging

class Worker:
    def __init__(self, result, trip_queue, callback, worker_object, result_queue):
        self.result_queue = result_queue
        self.trips = Trips(trip_queue, callback, result)
        self.worker_object = worker_object

    def run(self):
        work_result = self.worker_object.work()
        result = self.trips.trips(work_result)
        logging.info('result: {}'.format(result))
        send_results(result, self.result_queue)#TODO: add to configuration