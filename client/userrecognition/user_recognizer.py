import copy
import pickle
import time
from threading import Thread

import globals as glob
import socket_communication

class UserRecognizer(Thread):
    def __init__(self, frequency=1):
        super(UserRecognizer, self).__init__()
        self._frequency = frequency

    def run(self):
        while not glob.stop_flag:
            time.sleep(1 / self._frequency)
            with glob.shared_frame_lock:
                img = copy.deepcopy(glob.actual_frame)
            with glob.controller.socket_lock:
                socket_communication.send({"type": "user-recognition", "frame": img.tobytes()})
                reply = socket_communication.recv()
            user = pickle.loads(reply["payload"])
            print(reply)
            if user is not None:
                glob.logged_user = user
                glob.logged_user.set_mode(False)
                glob.controller.rotate_back_seat(glob.logged_user.get_position())
                return
