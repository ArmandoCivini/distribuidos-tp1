import logging
import json
from middleware.consumer import Consumer

class Stations(Consumer):
    def __init__(self, consumer_id):
        super().__init__(consumer_id, 'stations_exchange', '')
        self.keys = ['code', 'name', 'latitude', 'longitude']
        self.stations_montreal = self.add_keys(self.keys)
        self.stations_toronto = self.add_keys(self.keys)
        self.stations_washington = self.add_keys(self.keys)

    def get_stations(self):
        self.run()
        return [self.stations_montreal, self.stations_toronto, self.stations_washington]
    
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
            elif station['city'] == 'toronto':
                self.stations_toronto[column].extend(station[column])
            else:
                self.stations_washington[column].extend(station[column])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def work(self):
        return self.get_stations()