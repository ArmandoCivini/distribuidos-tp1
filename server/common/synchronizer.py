import logging
from common_middleware.consumer import Consumer

class Synchronizer(Consumer):
    def __init__(self):
        super().__init__(0, '', 'sync_queue')
        self.expected_responses = 4
        self.received_responses = 0

    def sync(self):
        self.run()
    
    def callback(self, ch, method, body):
        if body.decode("utf-8")  == 'finished':
            logging.info('received finished from worker')
            self.received_responses += 1
        if self.received_responses == self.expected_responses:
            ch.stop_consuming()
        ch.basic_ack(delivery_tag=method.delivery_tag)