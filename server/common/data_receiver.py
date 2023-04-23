from common.protocol import read_json
from common.column_filter import ColumnFilter
import logging

def data_receiver(skt):
    column_filter = ColumnFilter()
    data, error = read_json(skt)
    logging.info('sending data')#TODO: remove
    for i in range(100):
    # while data:
        column_filter.filter(data)
        data, error = read_json(skt)
    return error
