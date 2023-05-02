from common.protocol import read_json
from common.column_filter import ColumnFilter
import logging

class DataReceiver:
    def __init__(self):
        self.column_filter = ColumnFilter()

    def data_receiver(self, skt):
        column_filter = self.column_filter
        data, extra = read_json(skt)
        logging.info('sending data')#TODO: remove
        while extra != "finished" and extra != "error":
            if extra == "end of stations":
                logging.info('sending end of stations')#TODO: remove
                column_filter.send_end_stations()
            elif extra == "end of weather":
                logging.info('sending end of weather')#TODO: remove
                column_filter.send_end_weather()
            else:
                column_filter.filter(data)
            data, extra = read_json(skt)
        column_filter.send_end_trips()
        return extra
    
    def close(self):
        self.column_filter.close()
