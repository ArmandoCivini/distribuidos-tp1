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

def send_string(skt, string):
    len = len(string)
    write_int32(skt, len)
    long_write(skt, string)