import pika
import logging
import json
from common.post_process_results import post_process_results
import signal
import sys
import common.config as config

class ResultReducer:
    def __init__(self):
        #TODO: add to configuration
        self.results_stations_queue = config.STATIONS_RESULT_QUEUE
        self.results_weather_queue = config.WEATHER_RESULT_QUEUE
        self.station_result_total = config.STATIONS_WORKERS_COUNT
        self.weather_result_total = config.WEATHER_WORKERS_COUNT
        self.station_result_count = 0
        self.weather_result_count = 0
        self.is_error = False
        self.year_result = None
        self.montreal_result = None
        self.weather_result = {'count': 0, 'duration': 0}
        self.connection = pika.SelectConnection(
            pika.ConnectionParameters(host=config.RABBIT_HOST), on_open_callback=self.on_open)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        
    def on_open(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.basic_qos(prefetch_count=1)

        channel.queue_declare(queue=self.results_stations_queue)
        channel.queue_declare(queue=self.results_weather_queue)

        channel.basic_consume(queue=self.results_stations_queue, on_message_callback=self.callback_station_results)
        channel.basic_consume(queue=self.results_weather_queue, on_message_callback=self.callback_weather_results)

    def reduce(self):
        try:
            self.connection.ioloop.start()
        except:
            logging.info('error receiving results')
            self.connection.close()
            return
        self.connection.close()
        if self.is_error: return None ,config.ERROR_MESSAGE
        logging.info(f'finished consuming results: {self.year_result}, {self.montreal_result}, {self.weather_result}')
        results = post_process_results(self.year_result, self.montreal_result, self.weather_result)
        return results, 'success'

    def check_completed(self):
        if self.station_result_count >= self.station_result_total and self.weather_result_count >= self.weather_result_total:
            self.connection.ioloop.stop()

    def combine_results(self, new_result, old_result, key1, key2):
        if not new_result: return old_result
        if old_result == None:
            return new_result
        for key in new_result:
            if key not in old_result:
                old_result[key] = new_result[key]
            else:
                if key1 in old_result[key]: old_result[key][key1] += new_result[key][key1]
                if key2 in old_result[key]: old_result[key][key2] += new_result[key][key2]
        return old_result

    def combine_results_years(self, result_year):
        # self.year_result = self.combine_results(result_year, self.year_result, '2016', '2017')
        self.year_result = self.combine_results(result_year, self.year_result, config.YEAR1, config.YEAR2)

    def combine_results_montreal(self, result_montreal):
        self.montreal_result = self.combine_results(result_montreal, self.montreal_result, 'sum', 'count')
    
    def callback_station_results(self, ch, method, properties, body):
        try:
            result = json.loads(body)
        except:
            logging.error("failed to parse json: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        self.combine_results_years(result['year_count'])
        self.combine_results_montreal(result['total_distance'])
        self.station_result_count += 1
        self.check_completed()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_weather_results(self, ch, method, properties, body):
            logging.info(f"received weather result{body}")
            try:
                result = json.loads(body)
            except:
                logging.error("failed to parse json: %s", body)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            if result['duration']: self.weather_result['duration'] += result['duration']
            if result['count']: self.weather_result['count'] += result['count']
            self.weather_result_count += 1
            self.check_completed()
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass
    
    def graceful_shutdown(self, signum, frame):
        logging.info('received graceful shutdown signal')
        try:
            self.connection.close()
        except:
            pass
        sys.exit(0)

   