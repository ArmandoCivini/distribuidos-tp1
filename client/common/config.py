import json

def declare_config(config_params):
    global ERROR_MESSAGE
    global EOF
    global PREDATA_BATCH_SIZE
    global DATA_BATCH_SIZE
    global STATIONS_FILE_LIST
    global WEATHER_FILE_LIST
    global TRIPS_FILE_LIST
    global END_STATIONS_MESSAGE
    global END_WEATHER_MESSAGE
    ERROR_MESSAGE = json.loads(config_params["error_message"])
    EOF = json.loads(config_params["eof"])
    PREDATA_BATCH_SIZE = int(config_params["predata_batch_size"])
    DATA_BATCH_SIZE = int(config_params["data_batch_size"])
    STATIONS_FILE_LIST = json.loads(config_params["stations_file_list"])
    WEATHER_FILE_LIST = json.loads(config_params["weather_file_list"])
    TRIPS_FILE_LIST = json.loads(config_params["trips_file_list"])
    END_STATIONS_MESSAGE = json.loads(config_params["end_stations_message"])
    END_WEATHER_MESSAGE = json.loads(config_params["end_weather_message"])