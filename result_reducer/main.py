#!/usr/bin/env python3

from configparser import ConfigParser
from common.result_reducer import ResultReducer
import logging
import os
from common_middleware.result_sender import send_results
from common.config import declare_config
import json

def initialize_config():
    """ Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file. 
    If at least one of the config parameters is not found a KeyError exception 
    is thrown. If a parameter could not be parsed, a ValueError is thrown. 
    If parsing succeeded, the function returns a ConfigParser object 
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config.ini")

    config_params = {}
    try:
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["avg_ride"] = os.getenv('AVG_RIDE', config["DEFAULT"]["AVG_RIDE"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))
    
    config.read("middleware_config.ini")

    try:
        config_params["notif_queue"] = os.getenv('NOTIF_QUEUE', config["DEFAULT"]["NOTIF_QUEUE"])
        config_params["combined_results_queue"] = os.getenv('COMBINE_RESULTS_QUEUE', config["DEFAULT"]["COMBINE_RESULTS_QUEUE"])
        config_params["error_message"] = os.getenv('ERROR_MESSAGE', config["DEFAULT"]["ERROR_MESSAGE"])
        config_params["weather_workers_count"] = os.getenv('WEATHER_WORKERS_COUNT', config["DEFAULT"]["WEATHER_WORKERS_COUNT"])
        config_params["stations_workers_count"] = os.getenv('STATIONS_WORKERS_COUNT', config["DEFAULT"]["STATIONS_WORKERS_COUNT"])
        config_params["stations_result_queue"] = os.getenv('STATIONS_RESULT_QUEUE', config["DEFAULT"]["STATIONS_RESULT_QUEUE"])
        config_params["weather_result_queue"] = os.getenv('WEATHER_RESULT_QUEUE', config["DEFAULT"]["WEATHER_RESULT_QUEUE"])
        config_params["rabbit_host"] = os.getenv('RABBIT_HOST', config["DEFAULT"]["RABBIT_HOST"])
        config_params["year1"] = os.getenv('YEAR1', config["DEFAULT"]["YEAR1"])
        config_params["year2"] = os.getenv('YEAR2', config["DEFAULT"]["YEAR2"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params


def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]
    combined_results_queue = json.loads(config_params["combined_results_queue"])

    initialize_log(logging_level)
    declare_config(config_params)
    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | logging_level: {logging_level}")

    reducer = ResultReducer()
    results, status = reducer.reduce()
    logging.info(f'reducer results queso: {results}')
    if status == 'success':
        send_results(results, combined_results_queue)
    else:
        logging.info('error receiving results')
    logging.info('closing result reducer')

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


if __name__ == "__main__":
    main()
