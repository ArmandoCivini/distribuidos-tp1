from common.csv_parser import CsvParser
from common.protocol import send_string

def get_metadata(file):
    data = file.split("/")
    city = data[-2]
    type = data[-1].split(".")[0]
    meta_data = {"city":type, "type":city}
    return meta_data

def file_sender(skt, file):
    csv = CsvParser(file, get_metadata(file))
    line = csv.get_line_json()
    while line:
        send_string(skt, line) #TODO: catch socket close
        line = csv.get_line_json()
    return None