import json
import sys

sock = None


def send(data):
    json_data = json.dumps(data)
    # send the length in bytes of the message
    data = json_data.encode(encoding='utf-8')
    size_data = (len(data)).to_bytes(4, byteorder='little')
    sock.sendall(size_data)
    # send the message
    sock.sendall(data)


def recv():
    # recv data len
    data_size = int(sock.recv(4).decode())
    data_size = int.from_bytes(data_size, byteorder='little')
    # recv the data
    data = b''
    while len(data) < data_size:
        data = sock.recv(data_size - len(data))
        if not data:
            break  # Connection closed
        data += data

    data = data.decode('utf-8')
    return json.loads(data)


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
