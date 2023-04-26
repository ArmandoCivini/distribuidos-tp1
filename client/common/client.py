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

    def run(self):
        self.connect()
        #TODO: move to configuration
        file_list = ["/data/montreal/trips.csv"]
        for file in file_list:
            file_sender(self.sock, file)
        logging.info(f"ALL FILES SENT")
        send_string(self.sock, "eof")
        #TODO: close socket


