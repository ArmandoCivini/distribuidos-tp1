from haversine import haversine

def merge_trip_stations(trip, stations_montreal, stations_wt):
    if trip['start_station_code'] in stations_montreal['code']:
        city = 'montreal'
        indx = stations_montreal['code'].index(trip['start_station_code'])
    else:
        city = 'wt'
        indx = stations_wt['code'].index(trip['start_station_code'])
    return city, indx

def process_montreal(trip, stations, start_indx,curr_results):
    start_pos = (stations['latitude'][start_indx], stations['longitude'][start_indx])
    end_indx = stations['code'].index(trip['end_station_code'])
    end_pos = (stations['latitude'][end_indx], stations['longitude'][end_indx])
    distance = haversine(start_pos, end_pos, unit='km', axis=1)
    total_distance = curr_results['total_distance']
    end_station = stations['name'][end_indx]
    if end_station not in total_distance:
        total_distance[end_station] = {'sum':0, 'count':0}
    total_distance[end_station]['sum'] += distance
    total_distance[end_station]['count'] += 1
    curr_results['total_distance'] = total_distance
    return curr_results

def process_year(trip, stations, indx, curr_results):
    year = int(trip['start_date'].split('-')[0])
    year_count = curr_results['year_count']
    if year==2016 or year==2017:
        station = stations['name'][indx]
        if station not in year_count:
            year_count[station] = {2016: 0, 2017: 0}
        year_count[station][year] += 1
    curr_results['year_count'] = year_count
    return curr_results

def process_trips_stations(trip, stations, curr_results):
    stations_montreal, stations_wt = stations[0], stations[1]
    city, indx = merge_trip_stations(trip, stations_montreal, stations_wt)
    if city == 'montreal':
        curr_results = process_montreal(trip, stations_montreal, curr_results)
        curr_results = process_year(trip, stations_montreal, indx, curr_results)
    else:
        curr_results = process_year(trip, stations_wt, indx, curr_results)
    return curr_results  