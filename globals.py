import threading

from seatcomfortlogic.seat_comfort_controller import SeatComfortController

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

