import socket
from common.file_sender import file_sender
from common.protocol import send_string, read_string
import logging
import json
import signal
import sys
from time import sleep
class Client:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

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
        stations_file_list = ["/data/montreal/stations.csv", "/data/toronto/stations.csv", "/data/washington/stations.csv"]
        # stations_file_list = ["/data/montreal/stations.csv"]
        weather_file_list = ["/data/montreal/weather.csv", "/data/toronto/weather.csv", "/data/washington/weather.csv"]
        # weather_file_list = ["/data/montreal/weather.csv"]
        trips_file_list = ["/data/montreal/trips.csv", "/data/toronto/trips.csv", "/data/washington/trips.csv"]
        # trips_file_list = ["/data/montreal/trips.csv"]
        try:
            self.send_file_list(weather_file_list, "end of weather", 100)
            self.send_file_list(stations_file_list, "end of stations", 100)
            sleep(5)
            self.send_file_list(trips_file_list, "eof", 1)#TODO: change to 1000
            logging.info(f"ALL FILES SENT")
            self.receive_results()
        except socket.error as e:
            logging.error(f"Socket closed, gracefully shuting down")
            return
        
    def graceful_shutdown(self, signum, frame):
        logging.info(f"gracefully shutting down")
        send_string(self.sock, "error")
        try:
            self.sock.close()
        except:
            pass
        sys.exit(0)

    
    def __del__(self):
        try:
            logging.info('closing socket')
            self.sock.close()
        except:
            pass


