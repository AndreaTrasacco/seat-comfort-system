import copy
import os
import time
import globals as glob
from threading import Thread

from deepface import DeepFace

class UserRecognizer(Thread):
    def __init__(self, users_storage_controller):
        super(UserRecognizer, self).__init__()
        self._user_faces_dir = "../data/user_faces_db"
        self._users_storage_ctrl = users_storage_controller
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
        while True:
            time.sleep(1 / self._frequency)
            with glob.shared_frame_lock:
                img = copy.deepcopy(glob.actual_frame)
            user_name = self.detect_user(img)
            print("RESULT : " + user_name)
            if user_name is not None:
                glob.logged_user = self._users_storage_ctrl.retrieve_user(user_name)
                return
