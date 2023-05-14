#!/usr/bin/env python3

from configparser import ConfigParser
from common.server import Server
import logging
import os
from common.config import declare_config

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
        config_params["port"] = int(os.getenv('SERVER_PORT', config["DEFAULT"]["SERVER_PORT"]))
        config_params["listen_backlog"] = int(os.getenv('SERVER_LISTEN_BACKLOG', config["DEFAULT"]["SERVER_LISTEN_BACKLOG"]))
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["weather_columns"] = os.getenv('WEATHER_COLUMNS', config["DEFAULT"]["WEATHER_COLUMNS"])
        config_params["stations_columns"] = os.getenv('STATIONS_COLUMNS', config["DEFAULT"]["STATIONS_COLUMNS"])
        config_params["trips_columns"] = os.getenv('TRIPS_COLUMNS', config["DEFAULT"]["TRIPS_COLUMNS"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))
    
    config.read("middleware_config.ini")

    try:
        config_params["weather_type"] = os.getenv('WEATHER_TYPE', config["DEFAULT"]["WEATHER_TYPE"])
        config_params["stations_type"] = os.getenv('STATIONS_TYPE', config["DEFAULT"]["STATIONS_TYPE"])
        config_params["trips_type"] = os.getenv('TRIPS_TYPE', config["DEFAULT"]["TRIPS_TYPE"])
        config_params["weather_exchange"] = os.getenv('WEATHER_EXCHANGE', config["DEFAULT"]["WEATHER_EXCHANGE"])
        config_params["stations_exchange"] = os.getenv('STATIONS_EXCHANGE', config["DEFAULT"]["STATIONS_EXCHANGE"])
        config_params["trips_exchange"] = os.getenv('TRIPS_EXCHANGE', config["DEFAULT"]["TRIPS_EXCHANGE"])
        config_params["notif_exchange"] = os.getenv('NOTIF_EXCHANGE', config["DEFAULT"]["NOTIF_EXCHANGE"])
        config_params["weather_queue"] = os.getenv('WEATHER_QUEUE', config["DEFAULT"]["WEATHER_QUEUE"])
        config_params["stations_queue"] = os.getenv('STATIONS_QUEUE', config["DEFAULT"]["STATIONS_QUEUE"])
        config_params["trips_queue"] = os.getenv('TRIPS_QUEUE', config["DEFAULT"]["TRIPS_QUEUE"])
        config_params["notif_queue"] = os.getenv('NOTIF_QUEUE', config["DEFAULT"]["NOTIF_QUEUE"])
        config_params["trips_weather_queue"] = os.getenv('TRIPS_WEATHER_QUEUE', config["DEFAULT"]["TRIPS_WEATHER_QUEUE"])
        config_params["trips_stations_queue"] = os.getenv('TRIPS_STATIONS_QUEUE', config["DEFAULT"]["TRIPS_STATIONS_QUEUE"])
        config_params["end_message"] = os.getenv('END_MESSAGE', config["DEFAULT"]["END_MESSAGE"])
        config_params["end_trips_message"] = os.getenv('END_TRIPS_MESSAGE', config["DEFAULT"]["END_TRIPS_MESSAGE"])
        config_params["combine_results_exchange"] = os.getenv('COMBINE_RESULTS_EXCHANGE', config["DEFAULT"]["COMBINE_RESULTS_EXCHANGE"])
        config_params["combine_results_queue"] = os.getenv('COMBINE_RESULTS_QUEUE', config["DEFAULT"]["COMBINE_RESULTS_QUEUE"])
        config_params["sync_exchange"] = os.getenv('SYNC_EXCHANGE', config["DEFAULT"]["SYNC_EXCHANGE"])
        config_params["sync_queue"] = os.getenv('SYNC_QUEUE', config["DEFAULT"]["SYNC_QUEUE"])
        config_params["error_message"] = os.getenv('ERROR_MESSAGE', config["DEFAULT"]["ERROR_MESSAGE"])
        config_params["finished_message"] = os.getenv('FINISHED_MESSAGE', config["DEFAULT"]["FINISHED_MESSAGE"])
        config_params["end_stations_message"] = os.getenv('END_STATIONS_MESSAGE', config["DEFAULT"]["END_STATIONS_MESSAGE"])
        config_params["end_weather_message"] = os.getenv('END_WEATHER_MESSAGE', config["DEFAULT"]["END_WEATHER_MESSAGE"])
        config_params["eof"] = os.getenv('END_OF_FILE', config["DEFAULT"]["END_OF_FILE"])
        config_params["end_stations_message"] = os.getenv('END_STATIONS_MESSAGE', config["DEFAULT"]["END_STATIONS_MESSAGE"])
        config_params["end_weather_message"] = os.getenv('END_WEATHER_MESSAGE', config["DEFAULT"]["END_WEATHER_MESSAGE"])
        config_params["ok_message"] = os.getenv('OK_MESSAGE', config["DEFAULT"]["OK_MESSAGE"])
        config_params["weather_workers_count"] = os.getenv('WEATHER_WORKERS_COUNT', config["DEFAULT"]["WEATHER_WORKERS_COUNT"])
        config_params["stations_workers_count"] = os.getenv('STATIONS_WORKERS_COUNT', config["DEFAULT"]["STATIONS_WORKERS_COUNT"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params


def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]
    port = config_params["port"]
    listen_backlog = config_params["listen_backlog"]

    initialize_log(logging_level)
    declare_config(config_params)
    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | port: {port} | "
                  f"listen_backlog: {listen_backlog} | logging_level: {logging_level}")

    # Initialize server and start server loop
    server = Server(port, listen_backlog)
    server.run()
    logging.info('closing server')

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
