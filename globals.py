import json
import sys
import threading

from client.seatcomfortlogic.seat_comfort_controller import SeatComfortController

# lock to ensure mutual exclusion for the access of the frame
shared_frame_lock = threading.Lock()
actual_frame = None

# actual logged user
user_lock = threading.Lock()
logged_user = None

# lock for the seat position
seat_position_lock = threading.Lock()

# lock for the log
log_lock = threading.Lock()

# Flag to stop Threads
stop_flag: bool = False

controller = SeatComfortController()

sock = None


def send(data):
    json_data = json.dumps(data)
    # send the length in bytes of the message
    size_data = (get_size(json_data)).to_bytes(4, byteorder='little')
    sock.sendall(size_data)
    # send the message
    sock.sendall(json_data.encode())
    print('Message sent.')


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


class User:  # Model class
    def __init__(self, name, awake_position, sleep_position):
        self._name = name
        self._awake_position = awake_position
        self._sleep_position = sleep_position
        self._mode = False  # False: AWAKE, True: SLEEP

    def set_position(self, position):
        if not self._mode:  # if the actual mode is False, set the awake position depending on position argument
            self._awake_position = position
        else:  # if the actual mode is True, set the sleep position depending on position argument
            self._sleep_position = position

    def update_position_by_delta(self, delta):
        if not self._mode:  # if the actual mode is False, set the awake position updating it of the delta value
            self._awake_position += delta
        else:  # if the actual mode is True, set the sleep position updating it of the delta value
            self._sleep_position += delta

    def get_position(self):
        if not self._mode:
            return self._awake_position
        else:
            return self._sleep_position

    def get_mode(self):
        return self._mode

    def set_mode(self, mode):
        self._mode = mode

    def get_name(self):
        return self._name
