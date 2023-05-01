import logging
from datetime import datetime

def merge_trip_weather(trip, weather):
    date = datetime.strptime(trip['start_date'], "%Y-%m-%d %H:%M:%S").date()
    indx = weather['date'].index(date)
    prectot = weather['prectot'][indx]
    return float(prectot)

def process_trips_weather(trip, stations, curr_results):
    weather_montreal, weather_toronto, weather_washington = stations[0], stations[1], stations[2]
    if trip['city'] == 'montreal':
        weather = weather_montreal
    elif trip['city'] == 'toronto':
        weather = weather_toronto
    else:
        weather = weather_washington
    prectot = merge_trip_weather(trip, weather)
    if prectot > 30: #TODO: add to configuration
        duration = int(trip['duration_sec'])
        if duration < 0: duration = 0
        curr_results['duration'] += int(trip['duration_sec'])
        curr_results['count'] += 1
    return curr_results