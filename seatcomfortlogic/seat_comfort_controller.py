import threading
import time
import tkinter as tk

import numpy as np
import requests

from gui.camera_view import CameraView
from seatcomfortlogic.users_storage_controller import UsersStorageController

# lock to ensure mutual exclusion for the access of the frame
shared_frame = threading.Lock()
actual_frame = ""


class SeatComfortController:
    def __init__(self):
        # initialize the GUI
        self.master = tk.Tk()
        # self.textfield_view = TextFieldView(self.master)
        self.camera_view = CameraView(self.master)
        # self.right_side_view = RightSideView(self.master)

        self.camera_endpoint = "http://169.254.101.5:5000/Raspberry/photo"  # TODO mettere corretto

        self._users_storage_controller = UsersStorageController()
        self._users = self._users_storage_controller.retrieve_users()
        # self._need_detector = EyesDetector()
        # self._user_recognizer = UserRecognizer()

    def get_capture(self):
        while True:
            time.sleep(1) #TODO METTERE IN UNA COSTANTE
            response = requests.get(self.camera_endpoint)
            json_data = response.json()
            with shared_frame:
                actual_frame = np.array(json_data['photo'])
                self.camera_view.update_image(actual_frame)

    def main(self):
        # Create the view
        # Start thread for capturing frames
        camera_thread = threading.Thread(target=self.get_capture)
        camera_thread.daemon = True
        camera_thread.start()

        self.master.mainloop() # TODO FAR PARTIRE CON THREAD

    def signup_button_handler(self):
        name = self.textfield_view.get_text()
        # TODO GET img FROM CAMERA - ATTENTION
        img = []
        if name != '':
            self._user_recognizer.register_user(name, img)


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
