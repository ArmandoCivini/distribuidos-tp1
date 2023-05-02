import logging
from datetime import datetime

def merge_trip_weather(trip, weather):
    date = datetime.strptime(trip['start_date'], "%Y-%m-%d %H:%M:%S").date()
    indx = weather['date'].index(date)
    prectot = weather['prectot'][indx]
    return float(prectot)

def process_trips_weather(trip, weather, curr_results):
    # logging.info(f"chat trips: {trip}")
    weather_montreal, weather_toronto, weather_washington = weather[0], weather[1], weather[2]
    if trip['city'] == 'montreal':
        weather = weather_montreal
    elif trip['city'] == 'toronto':
        weather = weather_toronto
    else:
        weather = weather_washington
    prectot = merge_trip_weather(trip, weather)
    if prectot > 30: #TODO: add to configuration
        duration = float(trip['duration_sec'])
        if duration < 0: duration = 0
        curr_results['duration'] += duration
        curr_results['count'] += 1
    return curr_results