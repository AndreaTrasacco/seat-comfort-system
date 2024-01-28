import copy
import threading
import time
import tkinter as tk

from PIL import Image

import globals as glob
from eyesdetection.eyes_detector import EyesDetector
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
        self.master.wm_title("Seat Comfort System")
        self.textfield_view = None
        self.right_side_view = None
        self.camera_view = CameraView(self.master)

        self._users_storage_controller = UsersStorageController()
        self._need_detector_thread = EyesDetector(1, 5)
        self._camera_thread = ImagePickerClient()
        self._user_recognizer_thread = UserRecognizer(self._users_storage_controller)

    def main(self):
        self.textfield_view = TextFieldView(self.master)
        self.right_side_view = RightSideView(self.master)
        controller_thread = threading.Thread(target=self.run)  # start all the other threads
        controller_thread.start()
        self.master.mainloop()  # start the GUI
        glob.stop_flag = True
        if self._need_detector_thread.is_alive():
            self._need_detector_thread.join()
        if self._user_recognizer_thread.is_alive():
            self._user_recognizer_thread.join()
        if self._camera_thread.is_alive():
            self._camera_thread.join()
        if glob.logged_user is not None:
            self._users_storage_controller.save_user(glob.logged_user)

    def run(self):
        # Start thread for capturing frames
        self._camera_thread.start()
        time.sleep(10)
        # start the thread for the user recognition
        self._user_recognizer_thread.start()
        self._user_recognizer_thread.join()  # Wait for the user detection
        if not glob.stop_flag:
            self.change_button_status("signup", False)
            self.change_button_status("arrows", True)
            self.add_log_message(f"SEAT COMFORT SYSTEM - - User detected: " + glob.logged_user.get_name() + " (AWAKE)")
            self._need_detector_thread.start()

    def signup_button_handler(self):
        # handler for the signup button click
        name = self.textfield_view.get_text()
        with glob.shared_frame_lock:
            img = copy.deepcopy(glob.actual_frame)
        if name != '':
            img_pil = Image.fromarray(img)
            # save the captured frame, it must be used for the user recognition
            img_pil.save(self._user_faces_dir + "/" + name + ".jpg")
            new_user = User(name,
                            SeatComfortController.AWAKE_POSITION_DEFAULT,
                            SeatComfortController.SLEEPING_POSITION_DEFAULT)
            self._users_storage_controller.save_user(new_user)
            self.change_button_status("signup", False)

    def left_arrow_handler(self, event):
        # handler for the left arrows, must rotate the seat of 10 degrees
        self.rotate_back_seat(10)
        with glob.user_lock:
            glob.logged_user.update_position_by_delta(10)

    def right_arrow_handler(self, event):
        # handler for the right arrows, must rotate the seat of -10 degrees
        self.rotate_back_seat(-10)
        with glob.user_lock:
            glob.logged_user.update_position_by_delta(-10)

    def rotate_back_seat(self, degrees,
                         absolute=False):  # when absolute is True, an absolute value for the degrees is passed
        with glob.seat_position_lock:  # get the lock for changing the seat
            self.right_side_view.get_seat_view().rotate(degrees, absolute)

    def add_log_message(self, message):
        with glob.log_lock:  # get the lock for writing in the log text area
            self.right_side_view.get_log_view().add_message(message)

    def change_button_status(self, button, status):
        if button == "signup":
            self.textfield_view.change_button(status)
        elif button == "arrows":
            self.right_side_view.get_seat_view().change_button(status)

    def update_camera(self, img):
        # update the image on the camera area of the window
        self.camera_view.update_image(img)


if __name__ == '__main__':
    glob.controller.main()
