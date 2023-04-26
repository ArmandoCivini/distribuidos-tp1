from common.protocol import read_json
from common.column_filter import ColumnFilter
import logging

def data_receiver(skt):
    column_filter = ColumnFilter()
    data, extra = read_json(skt)
    logging.info('sending data')#TODO: remove
    for i in range(5):
    # while extra != "finished" and extra != "error":
        # logging.info(f'sending trip: {i}')#TODO: remove
        if extra == "end of stations":
            column_filter.send_end_stations()
        elif extra == "end of weather":
            column_filter.send_end_weather()
        else:
            column_filter.filter(data)
        data, extra = read_json(skt)
    column_filter.send_end_trips()
    return extra
