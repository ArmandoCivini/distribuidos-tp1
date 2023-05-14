import logging
import json
from common_middleware.consumer import Consumer
from datetime import datetime
import common.config as config

class Weather(Consumer):
    def __init__(self, consumer_id):
        super().__init__(consumer_id, config.WEATHER_EXCHANGE, config.WEATHER_QUEUE)
        self.keys = config.WEATHER_COLUMN_KEYS
        self.weather_montreal = self.add_keys(self.keys)
        self.weather_toronto = self.add_keys(self.keys)
        self.weather_washington = self.add_keys(self.keys)

    def get_weather(self):
        self.run()
        logging.info(f"finished consuming weather: {len(self.weather_montreal['date']) + len(self.weather_toronto['date']) + len(self.weather_washington['date'])}")
        self.post_processing()
        return [self.weather_montreal, self.weather_toronto, self.weather_washington]
    
    def callback(self, ch, method, body):
        if body.decode("utf-8")  == config.END_MESSAGE:
            logging.info('received end for weather')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.stop_consuming()
            return
        try:
            weather = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        for column in self.keys:
            if weather['city'] == config.MONTREAL_NAME:
                self.weather_montreal[column].extend(weather[column])
            elif weather['city'] == config.TORONTO_NAME:
                self.weather_toronto[column].extend(weather[column])
            else:
                self.weather_washington[column].extend(weather[column])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def post_processing_weather(self, weather):
        for i, date in enumerate(weather['date']):
            date = datetime.strptime(date, "%Y-%m-%d").date()
            weather['date'][i] = date
        return weather
    
    def post_processing(self):
        self.weather_montreal = self.post_processing_weather(self.weather_montreal)
        self.weather_toronto = self.post_processing_weather(self.weather_toronto)
        self.weather_washington = self.post_processing_weather(self.weather_washington)

    def work(self):
        return self.get_weather()