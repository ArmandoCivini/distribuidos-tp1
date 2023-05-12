import logging
from common_middleware.message_sender import send_message
from middleware.trips import Trips
from common_middleware.result_sender import send_results

class Worker:
    def __init__(self, result, trip_queue, callback, worker_object, result_queue):
        self.result_queue = result_queue
        self.trips = Trips(trip_queue, callback, result)
        self.worker_object = worker_object
        self.sync_queue = 'sync_queue'

    def run(self):
        work_result = self.worker_object.work()
        send_message('finished', self.sync_queue)
        result = self.trips.trips(work_result)
        logging.info('result: {}'.format(result))
        send_results(result, self.result_queue)#TODO: add to configuration