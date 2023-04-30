from common.protocol import read_json
from common.column_filter import ColumnFilter
import logging

def data_receiver(skt):
    column_filter = ColumnFilter()
    data, extra = read_json(skt)
    logging.info('sending data')#TODO: remove
    while extra != "finished" and extra != "error":
        if extra == "end of stations":
            logging.info('sending end of stations')#TODO: remove
            column_filter.send_end_stations()
        elif extra == "end of weather":
            column_filter.send_end_weather()
        else:
            column_filter.filter(data)
        data, extra = read_json(skt)
    column_filter.send_end_trips()
    return extra
