from datetime import datetime
import common.config as config

def merge_trip_weather(trip, weather):
    date = datetime.strptime(trip['start_date'], "%Y-%m-%d %H:%M:%S").date()
    indx = weather['date'].index(date)
    prectot = weather['prectot'][indx]
    return float(prectot)

def process_trips_weather(trip, weather, curr_results):
    weather_montreal, weather_toronto, weather_washington = weather[0], weather[1], weather[2]
    if trip['city'] == config.MONTREAL_NAME:
        weather = weather_montreal
    elif trip['city'] == config.TORONTO_NAME:
        weather = weather_toronto
    else:
        weather = weather_washington
    prectot = merge_trip_weather(trip, weather)
    if prectot > config.WEATHER_THRESHOLD:
        duration = float(trip['duration_sec'])
        if duration < 0: duration = 0
        curr_results['duration'] += duration
        curr_results['count'] += 1
    return curr_results