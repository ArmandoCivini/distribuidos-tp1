from haversine import haversine
import common.config as config

def merge_trip_stations(city, start_station_code, stations_montreal, stations_toronto, stations_washington):
    if city == config.MONTREAL_NAME:
        indx = stations_montreal['code'].index(start_station_code)
    elif city == config.TORONTO_NAME:
        indx = stations_toronto['code'].index(start_station_code)
    else:
        indx = stations_washington['code'].index(start_station_code)
    return indx

def get_pos(stations, indx):
    return (float(stations['latitude'][indx]), float(stations['longitude'][indx]))

def process_montreal(trip, stations, start_indx, curr_results):
    start_pos = get_pos(stations, start_indx)
    end_indx = stations['code'].index(trip['end_station_code'])
    end_pos = get_pos(stations, end_indx)
    distance = haversine(start_pos, end_pos, unit='km')
    total_distance = curr_results['total_distance']
    end_station = stations['name'][end_indx]
    if end_station not in total_distance:
        total_distance[end_station] = {'sum':0, 'count':0}
    total_distance[end_station]['sum'] += distance
    total_distance[end_station]['count'] += 1
    curr_results['total_distance'] = total_distance
    return curr_results

def process_year(trip, stations, indx, curr_results):
    year = trip['start_date'].split('-')[0]
    year_count = curr_results['year_count']
    if year==config.YEAR1 or year==config.YEAR2:
        station = stations['name'][indx]
        if station not in year_count:
            year_count[station] = {config.YEAR1: 0, config.YEAR2: 0}
        year_count[station][year] += 1
    curr_results['year_count'] = year_count
    return curr_results

def process_trips_stations(trip, stations, curr_results):
    stations_montreal, stations_toronto, stations_washington = stations[0], stations[1], stations[2]
    city = trip['city']
    indx = merge_trip_stations(city, trip['start_station_code'], stations_montreal, stations_toronto, stations_washington)
    if city == config.MONTREAL_NAME:
        curr_results = process_montreal(trip, stations_montreal, indx, curr_results)
        curr_results = process_year(trip, stations_montreal, indx, curr_results)
    elif city == config.TORONTO_NAME:
        curr_results = process_year(trip, stations_toronto, indx, curr_results)
    else:
        curr_results = process_year(trip, stations_washington, indx, curr_results)
    return curr_results  