import json
import logging
import common.config as config

def long_read(skt, n):
    #avoids short read
    message = []
    while len(message) < n:
        message += skt.recv(n)
    return message

def long_write(skt, message):
    #avoids short write
    while len(message) > 0:
        n = skt.send(message)
        message = message[n:]
    return message

def read_int32(skt):
    return int.from_bytes(long_read(skt, 4), byteorder='big', signed=True)

def write_int32(skt, int):
    long_write(skt, int.to_bytes(4, byteorder='big', signed=True))

def read_string(skt):
    len = read_int32(skt)
    return bytearray(long_read(skt, len)).decode('utf-8')

def send_string(skt, string):
    length = len(string)
    write_int32(skt, length)
    long_write(skt, string.encode('utf-8'))

def read_json(skt):
    msg = read_string(skt)
    if msg == config.END_OF_FILE:
        logging.info(f"client finished")
        return None, config.FINISHED_MESSAGE
    if msg == config.END_STATIONS_MESSAGE:
        logging.info(f"client finished sending stations")
        return None, config.END_STATIONS_MESSAGE
    if msg == config.END_WEATHER_MESSAGE:
        logging.info(f"client finished sending weather")
        return None, config.END_WEATHER_MESSAGE
    if msg == config.ERROR_MESSAGE:
        logging.error(f"client error")
        return None, config.ERROR_MESSAGE
    send_string(skt, config.OK_MESSAGE)
    return json.loads(msg), None