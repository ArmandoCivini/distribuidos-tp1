import pika
import logging
import json

class ResultReducer:
    def __init__(self):
        #TODO: add to configuration
        self.results_stations_queue = 'stations_result_queue'
        self.results_weather_queue = 'weather_result_queue'
        self.notif_exchange = 'notif_exchange'
        self.notif_queue = ''
        self.station_result_total = 0 #TODO: add to configuration
        self.weather_result_total = 2
        self.station_result_count = 0
        self.weather_result_count = 0
        self.is_error = False
        self.year_result = None
        self.montreal_result = None
        self.weather_result = None
        self.connection = pika.SelectConnection(
    pika.ConnectionParameters(host='rabbitmq'), on_open_callback=self.on_open)
        
    def on_open(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        channel.basic_qos(prefetch_count=1)

        channel.queue_declare(queue=self.results_stations_queue)
        channel.queue_declare(queue=self.results_weather_queue)

        channel.exchange_declare(callback=self.on_exchange_declareok_notif, exchange=self.notif_exchange, exchange_type='fanout')

        channel.basic_consume(queue=self.results_stations_queue, on_message_callback=self.callback_station_results)
        channel.basic_consume(queue=self.results_weather_queue, on_message_callback=self.callback_weather_results)

    def on_exchange_declareok_notif(self, frame):
        self.channel.queue_declare(self.notif_queue, callback=self.on_queue_declareok_notif)

    def on_queue_declareok_notif(self, frame):
        self.channel.queue_bind(self.notif_queue, self.notif_exchange, callback=self.on_bindok_notif)

    def on_bindok_notif(self, frame):
        self.channel.basic_consume(queue=self.notif_queue, on_message_callback=self.callback_notif)

    def reduce(self):
        try:
            self.connection.ioloop.start()
        except:
            logging.info('error receiving results')
            self.connection.close()
            return
        self.connection.close()
        if self.is_error: return 'error'
        logging.info(f'finished consuming results: {self.year_result}, {self.montreal_result}, {self.weather_result}')
        return 0#todo: return results

    def callback_notif(self, ch, method, properties, body):
        if body.decode("utf-8")  == 'error':
            logging.info('received end for results')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.connection.ioloop.stop()
            return
        logging.info("Received notif {}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

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
                old_result[key][key1] += new_result[key][key1]
                old_result[key][key2] += new_result[key][key2]
        return old_result

    def combine_results_years(self, result_year):
        self.year_result = self.combine_results(result_year, self.year_result, 2016, 2017)

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
            if self.weather_result == None:
                self.weather_result = result
            else:
                self.weather_result['duration'] += result['duration']
                self.weather_result['count'] += result['count']
            self.weather_result_count += 1
            self.check_completed()
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass


   