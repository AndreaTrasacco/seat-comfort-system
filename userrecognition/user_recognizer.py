import os
import time
from threading import Thread

from PIL import Image
from deepface import DeepFace
from seatcomfortlogic.seat_comfort_controller import stop_flag

class UserRecognizer(Thread):
    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"
        self._frequency = 1

    def detect_user(self, img):  # Returns the name of the user if it is registered, None otherwise
        recognition = DeepFace.find(img, db_path=self._user_faces_dir)
        if recognition[0].empty:  # User not recognized
            return None
        else:  # User recognized
            file_name = os.path.basename(recognition[0]["identity"][0])
            name, extension = os.path.splitext(file_name)
            user_name = name.split("/")[-1]
            return user_name

    def run(self):
        while not stop_flag:
            time.sleep(1/self._frequency)
            # TODO CONTINUE --> Take frame, call detect_user, if result != None --> return
