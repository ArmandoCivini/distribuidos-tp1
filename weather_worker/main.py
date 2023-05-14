#!/usr/bin/env python3
import os
import logging
from configparser import ConfigParser
from middleware.worker import Worker
from common.process_weather import process_trips_weather
from common.weather import Weather
from common.config import declare_config
import json

def initialize_config():

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config.ini")

    config_params = {}
    try:
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["weather_column_keys"] = os.getenv('WEATHER_COLUMN_KEYS', config["DEFAULT"]["WEATHER_COLUMN_KEYS"])
        config_params["weather_treshhold"] = os.getenv('WEATHER_TRESHHOLD', config["DEFAULT"]["WEATHER_TRESHHOLD"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    config.read("middleware_config.ini")

    try:
        config_params["montreal_name"] = os.getenv('MONTREAL_NAME', config["DEFAULT"]["MONTREAL_NAME"])
        config_params["toronto_name"] = os.getenv('TORONTO_NAME', config["DEFAULT"]["TORONTO_NAME"])
        config_params["weather_exchange"] = os.getenv('WEATHER_EXCHANGE', config["DEFAULT"]["WEATHER_EXCHANGE"])
        config_params["weather_queue"] = os.getenv('WEATHER_QUEUE', config["DEFAULT"]["WEATHER_QUEUE"])
        config_params["notif_exchange"] = os.getenv('NOTIF_EXCHANGE', config["DEFAULT"]["NOTIF_EXCHANGE"])
        config_params["trips_exchange"] = os.getenv('TRIPS_EXCHANGE', config["DEFAULT"]["TRIPS_EXCHANGE"])
        config_params["sync_queue"] = os.getenv('SYNC_QUEUE', config["DEFAULT"]["SYNC_QUEUE"])
        config_params["notif_queue"] = os.getenv('NOTIF_QUEUE', config["DEFAULT"]["NOTIF_QUEUE"])
        config_params["end_trips_message"] = os.getenv('END_TRIPS_MESSAGE', config["DEFAULT"]["END_TRIPS_MESSAGE"])
        config_params["finished_message"] = os.getenv('FINISHED_MESSAGE', config["DEFAULT"]["FINISHED_MESSAGE"])
        config_params["end_message"] = os.getenv('END_MESSAGE', config["DEFAULT"]["END_MESSAGE"])
        config_params["trips_weather_queue"] = json.loads(os.getenv('TRIPS_WEATHER_QUEUE', config["DEFAULT"]["TRIPS_WEATHER_QUEUE"]))
        config_params["weather_result_queue"] = json.loads(os.getenv('WEATHER_RESULT_QUEUE', config["DEFAULT"]["WEATHER_RESULT_QUEUE"]))
        config_params["rabbit_host"] = os.getenv('RABBIT_HOST', config["DEFAULT"]["RABBIT_HOST"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]

    initialize_log(logging_level)
    declare_config(config_params)

    logging.info('started worker')
    consumer_id = os.environ["WORKER_ID"]
    result = {'duration': 0, 'count': 0}
    worker_object = Weather(consumer_id)
    worker = Worker(result, config_params["trips_weather_queue"], process_trips_weather, worker_object, config_params["weather_result_queue"])
    worker.run()
    logging.info('closing worker')

    

if __name__ == "__main__":
    main()