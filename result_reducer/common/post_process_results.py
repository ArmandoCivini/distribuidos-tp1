import common.config as config

def post_process_weather(weather_result):
    if not weather_result:
        return 0
    if weather_result['count'] == 0:
        return 0
    return weather_result['duration']/weather_result['count']

def post_process_year(year_result):
    if not year_result:
        return []
    stations = []
    for station, years in year_result.items():
        if years[config.YEAR2] >= (years[config.YEAR1] * 2):
            stations.append(station)
    return stations

def post_process_montreal(montreal_result):
    if not montreal_result:
        return []
    stations = []
    for station, trips in montreal_result.items():
        if trips['count'] == 0: continue
        avg_ride = trips['sum']/trips['count']
        if avg_ride >= config.AVG_RIDE:
            stations.append(station)
    return stations
            
def post_process_results(year_result, montreal_result, weather_result):
    results = {}
    results['year'] = post_process_year(year_result)
    results['montreal'] = post_process_montreal(montreal_result)
    results['weather'] = post_process_weather(weather_result)
    return results