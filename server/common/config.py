import json

def declare_config(config_params):
    global WEATHER_COLUMNS
    global STATIONS_COLUMNS
    global TRIPS_COLUMNS
    global WEATHER_TYPE
    global STATIONS_TYPE
    global TRIPS_TYPE
    global WEATHER_EXCHANGE
    global STATIONS_EXCHANGE
    global TRIPS_EXCHANGE
    global NOTIF_EXCHANGE
    global WEATHER_QUEUE
    global STATIONS_QUEUE
    global TRIPS_QUEUE
    global NOTIF_QUEUE
    global TRIPS_WEATHER_QUEUE
    global TRIPS_STATIONS_QUEUE
    global END_MESSAGE
    global END_TRIPS_MESSAGE
    global COMBINE_RESULTS_EXCHANGE
    global COMBINE_RESULTS_QUEUE
    global SYNC_EXCHANGE
    global SYNC_QUEUE
    global ERROR_MESSAGE
    global FINISHED_MESSAGE
    global END_STATIONS_MESSAGE
    global END_WEATHER_MESSAGE
    global WORKERS_COUNT
    global END_OF_FILE
    global END_STATIONS_MESSAGE
    global END_WEATHER_MESSAGE
    global OK_MESSAGE
    global RABBIT_HOST
    WEATHER_COLUMNS = json.loads(config_params["weather_columns"])
    STATIONS_COLUMNS = json.loads(config_params["stations_columns"])
    TRIPS_COLUMNS = json.loads(config_params["trips_columns"])
    WEATHER_TYPE = config_params["weather_type"]
    STATIONS_TYPE = config_params["stations_type"]
    TRIPS_TYPE = config_params["trips_type"]
    WEATHER_EXCHANGE = json.loads(config_params["weather_exchange"])
    STATIONS_EXCHANGE = json.loads(config_params["stations_exchange"])
    TRIPS_EXCHANGE = json.loads(config_params["trips_exchange"])
    NOTIF_EXCHANGE = json.loads(config_params["notif_exchange"])
    WEATHER_QUEUE = json.loads(config_params["weather_queue"])
    STATIONS_QUEUE = json.loads(config_params["stations_queue"])
    TRIPS_QUEUE = json.loads(config_params["trips_queue"])
    NOTIF_QUEUE = json.loads(config_params["notif_queue"])
    TRIPS_WEATHER_QUEUE = json.loads(config_params["trips_weather_queue"])
    TRIPS_STATIONS_QUEUE = json.loads(config_params["trips_stations_queue"])
    END_MESSAGE = json.loads(config_params["end_message"])
    END_TRIPS_MESSAGE = json.loads(config_params["end_trips_message"])
    COMBINE_RESULTS_EXCHANGE = json.loads(config_params["combine_results_exchange"])
    COMBINE_RESULTS_QUEUE = json.loads(config_params["combine_results_queue"])
    SYNC_EXCHANGE = json.loads(config_params["sync_exchange"])
    SYNC_QUEUE = json.loads(config_params["sync_queue"])
    ERROR_MESSAGE = json.loads(config_params["error_message"])
    FINISHED_MESSAGE = json.loads(config_params["finished_message"])
    END_STATIONS_MESSAGE = json.loads(config_params["end_stations_message"])
    END_WEATHER_MESSAGE = json.loads(config_params["end_weather_message"])
    WORKERS_COUNT = int(config_params["weather_workers_count"]) + int(config_params["stations_workers_count"])
    END_OF_FILE = json.loads(config_params["eof"])
    END_STATIONS_MESSAGE = json.loads(config_params["end_stations_message"])
    END_WEATHER_MESSAGE = json.loads(config_params["end_weather_message"])
    OK_MESSAGE = json.loads(config_params["ok_message"])
    RABBIT_HOST = json.loads(config_params["rabbit_host"])