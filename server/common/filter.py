import common.config as config

def filter_columns(data, columns):
    filtered_data = {}
    for column in columns:
        filtered_data[column] = data[column]
    return filtered_data

def filter_data(data):
    if data['type'] == config.WEATHER_TYPE:
        columns = config.WEATHER_COLUMNS
    elif data['type'] == config.STATIONS_TYPE:
        columns = config.STATIONS_COLUMNS
    elif data['type'] == config.TRIPS_TYPE:
        columns = config.TRIPS_COLUMNS
    return filter_columns(data, columns)