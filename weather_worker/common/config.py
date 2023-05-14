import json

def declare_config(config_params):
    global MONTREAL_NAME
    global TORONTO_NAME
    global END_MESSAGE
    global WEATHER_EXCHANGE
    global WEATHER_QUEUE
    global WEATHER_COLUMN_KEYS
    global WEATHER_THRESHOLD
    global TRIPS_EXCHANGE
    global NOTIF_EXCHANGE
    global NOTIF_QUEUE
    global RABBIT_HOST
    global END_TRIPS_MESSAGE
    global SYNC_QUEUE
    global FINISHED_MESSAGE
    MONTREAL_NAME = json.loads(config_params["montreal_name"])
    TORONTO_NAME = json.loads(config_params["toronto_name"])
    END_MESSAGE = json.loads(config_params["end_message"])
    WEATHER_EXCHANGE = json.loads(config_params["weather_exchange"])
    WEATHER_QUEUE = json.loads(config_params["weather_queue"])
    WEATHER_COLUMN_KEYS = json.loads(config_params["weather_column_keys"])
    WEATHER_THRESHOLD = json.loads(config_params["weather_treshhold"])
    TRIPS_EXCHANGE = json.loads(config_params["trips_exchange"])
    NOTIF_EXCHANGE = json.loads(config_params["notif_exchange"])
    NOTIF_QUEUE = json.loads(config_params["notif_queue"])
    RABBIT_HOST = json.loads(config_params["rabbit_host"])
    END_TRIPS_MESSAGE = json.loads(config_params["end_trips_message"])
    SYNC_QUEUE = json.loads(config_params["sync_queue"])
    FINISHED_MESSAGE = json.loads(config_params["finished_message"])
    