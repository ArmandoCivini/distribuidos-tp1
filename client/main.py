#!/usr/bin/env python3

from configparser import ConfigParser
from common.client import Client
import logging
import os
from common.config import declare_config

def initialize_config():

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config.ini")

    config_params = {}
    try:
        config_params["port"] = int(os.getenv('SERVER_PORT', config["DEFAULT"]["SERVER_PORT"]))
        config_params["ip"] = os.getenv('SERVER_IP', config["DEFAULT"]["SERVER_IP"])
        config_params["logging_level"] = os.getenv('LOGGING_LEVEL', config["DEFAULT"]["LOGGING_LEVEL"])
        config_params["predata_batch_size"] = os.getenv('PREDATA_BATCH_SIZE', config["DEFAULT"]["PREDATA_BATCH_SIZE"])
        config_params["data_batch_size"] = os.getenv('DATA_BATCH_SIZE', config["DEFAULT"]["DATA_BATCH_SIZE"])
        config_params["stations_file_list"] = os.getenv('STATIONS_FILE_LIST', config["DEFAULT"]["STATIONS_FILE_LIST"])
        config_params["weather_file_list"] = os.getenv('WEATHER_FILE_LIST', config["DEFAULT"]["WEATHER_FILE_LIST"])
        config_params["trips_file_list"] = os.getenv('TRIPS_FILE_LIST', config["DEFAULT"]["TRIPS_FILE_LIST"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    config.read("middleware_config.ini")

    try:
        config_params["error_message"] = os.getenv('ERROR_MESSAGE', config["DEFAULT"]["ERROR_MESSAGE"])
        config_params["eof"] = os.getenv('END_OF_FILE', config["DEFAULT"]["END_OF_FILE"])
        config_params["end_stations_message"] = os.getenv('END_STATIONS_MESSAGE', config["DEFAULT"]["END_STATIONS_MESSAGE"])
        config_params["end_weather_message"] = os.getenv('END_WEATHER_MESSAGE', config["DEFAULT"]["END_WEATHER_MESSAGE"])
        config_params["ok_message"] = os.getenv('OK_MESSAGE', config["DEFAULT"]["OK_MESSAGE"])
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params


def main():
    config_params = initialize_config()
    logging_level = config_params["logging_level"]
    port = config_params["port"]
    ip = config_params["ip"]

    initialize_log(logging_level)
    declare_config(config_params)
    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug(f"action: config | result: success | port: {port} | "
                  f" logging_level: {logging_level}")

    # Initialize server and start server loop
    server = Client(port, ip)
    server.run()

def initialize_log(logging_level):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == "__main__":
    main()
