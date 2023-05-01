import socket
from common.file_sender import file_sender
from common.protocol import send_string, read_string
import logging
import json

class Client:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip

    def connect(self):
        #TODO: check for error
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def send_file_list(self, file_list, end, batch):
        for file in file_list:
            file_sender(self.sock, file, batch)
        send_string(self.sock, end)

    def receive_results(self):
        result_string = read_string(self.sock)
        if result_string == "error":
            logging.error("error in results")
            return
        result =  json.loads(result_string)
        logging.info(f"RESULT: {result}")

    def run(self):
        self.connect()
        #TODO: move to configuration
        stations_file_list = ["/data/montreal/stations.csv"]
        weather_file_list = ["/data/montreal/weather.csv"]
        trips_file_list = ["/data/montreal/trips.csv"]
        self.send_file_list(stations_file_list, "end of stations", 100)
        self.send_file_list(weather_file_list, "end of weather", 100)
        self.send_file_list(trips_file_list, "eof", 1)
        logging.info(f"ALL FILES SENT")
        result = self.receive_results()
        #TODO: close socket
    
    def __del__(self):
        try:
            logging.info('closing socket')
            self.sock.close()
        except:
            pass


