from common.protocol import read_json
from common.column_filter import column_filter

def data_receiver(skt):
    data, error = read_json(skt)
    while data:
        column_filter(data)
        data, error = read_json(skt)
    return error
