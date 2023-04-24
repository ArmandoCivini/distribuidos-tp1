import socket
import logging
from common.data_receiver import data_receiver

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

    def run(self):
        # TODO: Modify this program to handle signal to graceful shutdown
        # the server
        client_sock = self.__accept_new_connection()
        self.__handle_client_connection(client_sock)

    def __handle_client_connection(self, client_sock):
        try:
            error = data_receiver(client_sock)
            if error: logging.info(f"{error}")
        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
            client_sock.close()

    def __accept_new_connection(self):
        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c
