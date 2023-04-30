from common.csv_parser import CsvParser
from common.protocol import send_string, read_string
import logging

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
        send_string(skt, line) #TODO: catch socket close
        msg = read_string(skt) #TODO: catch socket close
        if msg == "error":
            return "error"
        line = csv.get_line_json()
    return None