import ast

sock = None


def send(data):
    # send the length in bytes of the message
    data = str(data).encode(encoding='utf-8')
    size_data = (len(data)).to_bytes(4, byteorder='little')
    sock.sendall(size_data)
    # send the message
    sock.sendall(data)


def recv():
    # recv data len
    data_size = sock.recv(4)
    if not data_size:
        raise BrokenPipeError  # Connection closed
    data_size = int.from_bytes(data_size, byteorder='little')
    # recv the data
    msg_data = b''
    while len(msg_data) < data_size:
        data = sock.recv(data_size - len(msg_data))
        if not data:
            raise BrokenPipeError  # Connection closed
        msg_data += data
    return ast.literal_eval(msg_data.decode('utf-8'))
