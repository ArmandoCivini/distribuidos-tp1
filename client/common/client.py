import socket
from common.file_sender import file_sender
from middleware.protocol import send_string, read_string
import logging
import json
import signal
import sys
import common.config as config

class Client:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
        except socket.error as e:
            logging.error(f"Error connecting to server: {e}")
            sys.exit(0)

    def send_file_list(self, file_list, end, batch):
        for file in file_list:
            file_sender(self.sock, file, batch)
        send_string(self.sock, end)

    def receive_results(self):
        result_string = read_string(self.sock)
        if result_string == config.ERROR_MESSAGE:
            logging.error("error in results")
            return
        result =  json.loads(result_string)
        logging.info(f"RESULT: {result}")

    def run(self):
        self.connect()
        stations_file_list = config.STATIONS_FILE_LIST
        weather_file_list = config.WEATHER_FILE_LIST
        trips_file_list = config.TRIPS_FILE_LIST

        try:
            self.send_file_list(stations_file_list, config.END_STATIONS_MESSAGE, config.PREDATA_BATCH_SIZE) #this order has to be maintained
            self.send_file_list(weather_file_list, config.END_WEATHER_MESSAGE, config.PREDATA_BATCH_SIZE)

            logging.info(f"SENDING TRIPS")
            self.send_file_list(trips_file_list, config.EOF, config.DATA_BATCH_SIZE)
            logging.info(f"ALL FILES SENT")
            self.receive_results()
        except socket.error as e:
            logging.error(f"Socket closed, gracefully shuting down")
            return
        
    def graceful_shutdown(self, signum, frame):
        logging.info(f"gracefully shutting down")
        send_string(self.sock, config.ERROR_MESSAGE)
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


