import json

def declare_config(config_params):
    global NOTIF_QUEUE
    global ERROR_MESSAGE
    global WEATHER_WORKERS_COUNT
    global STATIONS_WORKERS_COUNT
    global STATIONS_RESULT_QUEUE
    global WEATHER_RESULT_QUEUE
    global RABBIT_HOST
    global YEAR1
    global YEAR2
    global AVG_RIDE
    NOTIF_QUEUE = json.loads(config_params["notif_queue"])
    ERROR_MESSAGE = json.loads(config_params["error_message"])
    WEATHER_WORKERS_COUNT = int(config_params["weather_workers_count"]) 
    STATIONS_WORKERS_COUNT = int(config_params["stations_workers_count"])
    STATIONS_RESULT_QUEUE = json.loads(config_params["stations_result_queue"])
    WEATHER_RESULT_QUEUE = json.loads(config_params["weather_result_queue"])
    RABBIT_HOST = json.loads(config_params["rabbit_host"])
    YEAR1 = json.loads(config_params["year1"])
    YEAR2 = json.loads(config_params["year2"])
    AVG_RIDE = int(config_params["avg_ride"])