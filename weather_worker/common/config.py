import json

def declare_config(config_params):
    # global YEAR1
    # global YEAR2
    global MONTREAL_NAME
    global TORONTO_NAME
    # global STATIONS_KEYS
    # global STATIONS_EXCHANGE
    # global STATIONS_QUEUE
    global END_MESSAGE
    global WEATHER_EXCHANGE
    global WEATHER_QUEUE
    global WEATHER_COLUMN_KEYS
    global WEATHER_THRESHOLD
    # YEAR1 = json.loads(config_params["year1"])
    # YEAR2 = json.loads(config_params["year2"])
    MONTREAL_NAME = json.loads(config_params["montreal_name"])
    TORONTO_NAME = json.loads(config_params["toronto_name"])
    # STATIONS_KEYS = json.loads(config_params["stations_keys"])
    # STATIONS_EXCHANGE = json.loads(config_params["stations_exchange"])
    # STATIONS_QUEUE = json.loads(config_params["stations_queue"])
    END_MESSAGE = json.loads(config_params["end_message"])
    WEATHER_EXCHANGE = json.loads(config_params["weather_exchange"])
    WEATHER_QUEUE = json.loads(config_params["weather_queue"])
    WEATHER_COLUMN_KEYS = json.loads(config_params["weather_column_keys"])
    WEATHER_THRESHOLD = json.loads(config_params["weather_treshhold"])