#!/usr/bin/env python3
import pika
import time
import os
import logging
from configparser import ConfigParser
from common.stations import Stations
from common.split import split
def initialize_config():

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config.ini")

    config_params = {}
    try:
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
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

    logging.info('started worker')
    weather_exchange = 'weather_exchange'
    trips_exchange = 'trips_exchange'
    consumer_id = os.environ["WORKER_ID"]
    split()
    # stations = Stations(consumer_id)
    # stations.run()
    

if __name__ == "__main__":
    main()