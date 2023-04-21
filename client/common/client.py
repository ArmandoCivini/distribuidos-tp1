import socket
from common.csv_parser import CsvParser
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
        csv = CsvParser("/data/montreal/stations.csv")
        self.sock.send("{}\n".format(csv.get_line_json()).encode('utf-8'))
        msg = self.sock.recv(1024).rstrip().decode('utf-8')
        print(msg)