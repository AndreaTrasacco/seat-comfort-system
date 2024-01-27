import copy
import threading
import time
import tkinter as tk
import global_start as glob

from PIL import Image

from gui.camera_view import CameraView
from gui.rigth_side_view import RightSideView
from gui.textfield_view import TextFieldView
from imagepicker.image_picker_client import ImagePickerClient
from seatcomfortlogic.users_storage_controller import UsersStorageController, User
from userrecognition.user_recognizer import UserRecognizer

class SeatComfortController:
    AWAKE_POSITION_DEFAULT = 0  # Position of the back seat when the user is awake
    SLEEPING_POSITION_DEFAULT = 60  # Degrees w.r.t "awake position" of the back seat when the user is sleeping

    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"
        # initialize the GUI
        self.master = tk.Tk()
        self.textfield_view = TextFieldView(self.master, self)
        self.camera_view = CameraView(self.master)
        self.right_side_view = RightSideView(self.master, self)

        self.camera_endpoint = "http://169.254.101.5:5000/Raspberry/photo"  # TODO mettere corretto

        self._users_storage_controller = UsersStorageController()
        # self._need_detector = EyesDetector()
        self._camera_thread = ImagePickerClient()
        self._user_recognizer_thread = UserRecognizer(self._users_storage_controller)

    def main(self):
        global stop_flag
        controller_thread = threading.Thread(target=self.run)
        controller_thread.start()
        self.master.mainloop()
        stop_flag = True  # TODO TESTARE
        self._camera_thread.join()  # TODO FOR ALL THE THREADS
        if glob.logged_user is not None:
            self._users_storage_controller.save_user(glob.logged_user)

    def run(self):
        # Start thread for capturing frames
        self._camera_thread.start()
        time.sleep(10)
        self._user_recognizer_thread.start()
        self._user_recognizer_thread.join()  # Wait for the user detection
        self.add_log_message("USER DETECTED : " + glob.logged_user.get_name())
        # TODO Start other threads
        # TODO ATTENZIONE BOTTONI

    def signup_button_handler(self):
        name = self.textfield_view.get_text()
        with glob.shared_frame_lock:
            img = copy.deepcopy(glob.actual_frame)
        if name != '':
            img_pil = Image.fromarray(img)
            img_pil.save(self._user_faces_dir + "/" + name + ".jpg")
            new_user = User(name,
                            SeatComfortController.AWAKE_POSITION_DEFAULT,
                            SeatComfortController.SLEEPING_POSITION_DEFAULT)
            self._users_storage_controller.save_user(new_user)
            # TODO ATTENZIONE BOTTONI

    def left_arrow_handler(self, event):
        self.rotate_back_seat(10)
        pass

    def right_arrow_handler(self, event):
        self.rotate_back_seat(-10)
        pass

    def rotate_back_seat(self, degrees, absolute=False):
        with glob.seat_position_lock:
            self.right_side_view.get_seat_view().rotate(degrees, absolute)
        # TODO UPDATE USER

    def add_log_message(self, message):
        with glob.log_lock:
            self.right_side_view.get_log_view().add_message(message)

if __name__ == '__main__':
    glob.controller.main()

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
