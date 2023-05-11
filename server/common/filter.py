def filter_columns(data, columns):
    filtered_data = {}
    for column in columns:
        filtered_data[column] = data[column]
    return filtered_data

def filter_data(data):
    if data['type'] == 'weather':
        columns = ['city', 'date', 'prectot'] #TODO: add to configuration
    elif data['type'] == 'stations':
        columns = ['city', 'code', 'name', 'latitude', 'longitude'] #TODO: add to configuration
    elif data['type'] == 'trips':
        columns = ['city', 'start_date', 'start_station_code', 'end_station_code', 'duration_sec'] #TODO: add to configuration
    return filter_columns(data, columns)