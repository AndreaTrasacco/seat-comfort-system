import copy
import json
import socket
import threading
import time
import tkinter as tk

import numpy as np
from PIL import Image

from gui.camera_view import CameraView
from gui.rigth_side_view import RightSideView
from imagepicker.image_picker_client import ImagePickerClient
from seatcomfortlogic.users_storage_controller import UsersStorageController, User
from userrecognition.user_recognizer import UserRecognizer

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


class SeatComfortController:
    AWAKE_POSITION_DEFAULT = 0  # Position of the back seat when the user is awake
    SLEEPING_POSITION_DEFAULT = 60  # Degrees w.r.t "awake position" of the back seat when the user is sleeping

    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"
        # initialize the GUI
        self.master = tk.Tk()
        # self.textfield_view = TextFieldView(self.master)
        self.camera_view = CameraView(self.master)
        self.right_side_view = RightSideView(self.master)

        self.camera_endpoint = "http://169.254.101.5:5000/Raspberry/photo"  # TODO mettere corretto

        self._users_storage_controller = UsersStorageController()
        # self._need_detector = EyesDetector()
        # self._user_recognizer = UserRecognizer()
        self._camera_thread = ImagePickerClient()

    def main(self):
        # Create the view
        # Start thread for capturing frames
        camera_thread = threading.Thread(target=self.get_capture)
        camera_thread.daemon = True
        camera_thread.start()

        user_recognizer_thread = UserRecognizer()
        user_recognizer_thread.start()

        user_recognizer_thread.join()  # Wait for the user detection

        self.master.mainloop()  # TODO FAR PARTIRE CON THREAD
        stop_flag = True
        camera_thread.join()  # TODO FOR ALL THE THREADS
        if logged_user is not None:
            self._users_storage_controller.save_user(logged_user)

    def run(self):
        pass


    def signup_button_handler(self):
        name = self.textfield_view.get_text()
        with shared_frame_lock:
            img = copy.deepcopy(actual_frame)
        if name != '':
            img_pil = Image.fromarray(img)
            img_pil.save(self._user_faces_dir + "/" + name + ".jpg")
            new_user = User(name,
                            SeatComfortController.AWAKE_POSITION_DEFAULT,
                            SeatComfortController.SLEEPING_POSITION_DEFAULT)
            self._users_storage_controller.save_user(new_user)

    def left_arrow_handler(self, event):
        self.rotate_back_seat(10)
        pass

    def right_arrow_handler(self, event):
        self.rotate_back_seat(-10)
        pass

    def rotate_back_seat(self, degrees, absolute=False):
        with seat_position_lock:
            self.right_side_view.get_seat_view().rotate(degrees, absolute)

    def add_log_message(self, message):
        with log_lock:
            self.right_side_view.get_log_view().add_message(message)


if __name__ == '__main__':
    SeatComfortController().main()

'''
constant FRAME_FREQUENCY
--> PRINT EVERYTHING ON THE LOG TEXTAREA
Logic:
    1)  User Recognition: 
        [Whenever the new user clicks "Signup" button a frame is captured and the user is stored]
        Until user is not recognized
            Each frame is used as input to user recognition module
        Change the position of the seat to the preferred one for the user when he/she is awake
        Disable signup button
    2)  Need Detection:
        Until a *different* need is not detected (N consecutive frames of the same class)
            Each frame is used as input to eyes detection
        Change the position of the seat to the preferred one for the user (depending on the detected class)
    3)  Mood Detection:
        For M consecutive frames AFTER NEED DETECTION:
            If a "bad" emotion is detected 
                Restore the position
                Break
    Whenever the user changes the seat position manually --> store the new preferred position
'''
