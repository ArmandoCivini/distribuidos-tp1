import socket
import logging
from common.data_receiver import DataReceiver
from common.result_reducer import ResultReducer
from common.send_results import send_results
import sys
import signal

class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.result_reducer = ResultReducer()
        self.data_receiver = DataReceiver()
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

    def run(self):
        # the server
        client_sock = self.__accept_new_connection()
        self.__handle_client_connection(client_sock)

    def __handle_client_connection(self, client_sock):
        try:
            error = self.data_receiver.data_receiver(client_sock)
            if error: 
                logging.info(f"error in client")
                self.graceful_shutdown(None, None)
            result, error = self.result_reducer.reduce()
            send_results(client_sock, result, error)
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
    
    def graceful_shutdown(self, signum, frame):
        logging.info(f"gracefully shutting down")
        try:
            self.data_receiver.close()
            self._server_socket.close()
        except:
            pass
        sys.exit(0)
    
    def close(self):
        try:
            self._server_socket.close()
        except:
            logging.error('action: close_server | result: fail')
