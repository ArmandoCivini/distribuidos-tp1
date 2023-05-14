import json

def declare_config(config_params):
    global YEAR1
    global YEAR2
    global MONTREAL_NAME
    global TORONTO_NAME
    global STATIONS_KEYS
    global STATIONS_EXCHANGE
    global STATIONS_QUEUE
    global END_MESSAGE
    global TRIPS_EXCHANGE
    global NOTIF_EXCHANGE
    global NOTIF_QUEUE
    global RABBIT_HOST
    global END_TRIPS_MESSAGE
    global SYNC_QUEUE
    global FINISHED_MESSAGE
    YEAR1 = json.loads(config_params["year1"])
    YEAR2 = json.loads(config_params["year2"])
    MONTREAL_NAME = json.loads(config_params["montreal_name"])
    TORONTO_NAME = json.loads(config_params["toronto_name"])
    STATIONS_KEYS = json.loads(config_params["stations_keys"])
    STATIONS_EXCHANGE = json.loads(config_params["stations_exchange"])
    STATIONS_QUEUE = json.loads(config_params["stations_queue"])
    END_MESSAGE = json.loads(config_params["end_message"])
    TRIPS_EXCHANGE = json.loads(config_params["trips_exchange"])
    NOTIF_EXCHANGE = json.loads(config_params["notif_exchange"])
    NOTIF_QUEUE = json.loads(config_params["notif_queue"])
    RABBIT_HOST = json.loads(config_params["rabbit_host"])
    END_TRIPS_MESSAGE = json.loads(config_params["end_trips_message"])
    SYNC_QUEUE = json.loads(config_params["sync_queue"])
    FINISHED_MESSAGE = json.loads(config_params["finished_message"])