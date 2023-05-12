import logging
from common_middleware.consumer import Consumer
import common.config as config

class Synchronizer(Consumer):
    def __init__(self):
        super().__init__(0, config.SYNC_EXCHANGE, config.SYNC_QUEUE)
        self.expected_responses = config.WORKERS_COUNT
        self.received_responses = 0

    def sync(self):
        self.run()
    
    def callback(self, ch, method, body):
        if body.decode("utf-8")  == config.FINISHED_MESSAGE:
            logging.info('received finished from worker')
            self.received_responses += 1
        if self.received_responses == self.expected_responses:
            ch.stop_consuming()
        ch.basic_ack(delivery_tag=method.delivery_tag)