import logging
import json
from common_extra.consumer import Consumer

class Stations(Consumer):
    def __init__(self, consumer_id):
        super().__init__(consumer_id, 'stations_exchange', '')
        # self.stations_exchange = 'stations_exchange'
        # self.stations_queue = ''
        self.keys = ['code', 'name', 'latitude', 'longitude']
        self.stations_montreal = self.add_keys(self.keys)
        self.stations_wt = self.add_keys(self.keys)

    def get_stations(self):
        self.run()
        logging.info(f"finished consuming stations: {len(self.stations_montreal['code']) + len(self.stations_wt['code'])}")
        return self.stations_montreal, self.stations_wt
    
    def callback(self, ch, method, body):
        if body.decode("utf-8")  == 'end':
            logging.info('received end for stations')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()
            return
        try:
            station = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        for column in self.keys:
            if station['city'] == 'montreal':
                self.stations_montreal[column].extend(station[column])
            else:
                self.stations_wt[column].extend(station[column])
        ch.basic_ack(delivery_tag=method.delivery_tag)