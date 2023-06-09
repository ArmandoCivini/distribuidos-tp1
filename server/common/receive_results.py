from common_middleware.consumer import Consumer
import logging
import json
import common.config as config

class ReceiveResults(Consumer):
    def __init__(self):
        super().__init__(0, config.COMBINE_RESULTS_EXCHANGE, config.COMBINE_RESULTS_QUEUE)
        self.result = None

    def get_result(self):
        self.run()
        return self.result
    
    def callback(self, ch, method, body):
        try:
            result = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()
            return

        self.result = result
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming()