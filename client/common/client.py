import socket
from common.file_sender import file_sender
from common.protocol import send_string
import logging

class Client:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip

    def connect(self):
        #TODO: check for error
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def send_file_list(self, file_list, end):
        for file in file_list:
            file_sender(self.sock, file)
        send_string(self.sock, end)

    def run(self):
        self.connect()
        #TODO: move to configuration
        stations_file_list = ["/data/montreal/stations.csv"]
        weather_file_list = ["/data/montreal/weather.csv"]
        trips_file_list = ["/data/montreal/trips.csv"]
        # send_string(self.sock, "end of stations")
        self.send_file_list(stations_file_list, "end of stations")
        # self.send_file_list(weather_file_list, "end of weather")
        self.send_file_list(trips_file_list, "eof")
        logging.info(f"ALL FILES SENT")
        #TODO: close socket
    
    def __del__(self):
        try:
            logging.info('closing socket')
            self.sock.close()
        except:
            pass


