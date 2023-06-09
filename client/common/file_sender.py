from common.csv_parser import CsvParser
from middleware.protocol import send_string, read_string
import common.config as config

def get_metadata(file):
    data = file.split("/")
    city = data[-2]
    type = data[-1].split(".")[0]
    meta_data = {"city":city, "type":type}
    return meta_data

def file_sender(skt, file, batch):
    csv = CsvParser(file, get_metadata(file), batch)
    line = csv.get_line_json()
    while line:
        try:
            send_string(skt, line)
            msg = read_string(skt)
        except:
            return config.ERROR_MESSAGE
        if msg == config.ERROR_MESSAGE:
            return config.ERROR_MESSAGE
        line = csv.get_line_json()
    return None