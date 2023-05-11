#!/usr/bin/env python3
import os
import logging
from configparser import ConfigParser
from common_extra.worker import Worker
from common.stations import Stations
from common.process_station import process_trips_stations

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
    consumer_id = os.environ["WORKER_ID"]
    worker_object = Stations(consumer_id)
    result = {'year_count':{}, 'total_distance': {}}
    worker = Worker(result, 'trips_stations_queue', process_trips_stations, worker_object, 'stations_result_queue')
    worker.run()
    logging.info('closing worker')

    

if __name__ == "__main__":
    main()