import copy
import json
import socket
import threading
import time
import tkinter as tk

import numpy as np

from gui.camera_view import CameraView
from seatcomfortlogic.users_storage_controller import UsersStorageController, User

# lock to ensure mutual exclusion for the access of the frame
shared_frame = threading.Lock()
actual_frame = None


class SeatComfortController:
    AWAKE_POSITION_DEFAULT = 0  # Position of the back seat when the user is awake
    SLEEPING_POSITION_DEFAULT = 60  # Degrees w.r.t "awake position" of the back seat when the user is sleeping

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
        # Server configuration
        host = '169.254.101.5'
        port = 8000

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))

        try:
            while True:
                time.sleep(0.05)  # TODO METTERE IN UNA COSTANTE
                # Send a message to the server
                message_to_send = {"message": "request_for_photo"}
                client_socket.send(json.dumps(message_to_send).encode())
                # Receive the welcome message from the server

                # Receive the actual image data
                # image_data = client_socket.recv(1555200)
                image_data = b''
                while len(image_data) < 1555200:
                    data = client_socket.recv(1555200 - len(image_data))
                    if not data:
                        break  # Connection closed
                    image_data += data

                # Convert the received data to a numpy array
                image_np = np.frombuffer(image_data, dtype=np.uint8)
                # Reshape the NumPy array to the original image shape
                image = image_np.reshape((960, 540, 3))
                with shared_frame:
                    actual_frame = image
                    self.camera_view.update_image(actual_frame)

        except KeyboardInterrupt:
            print("Client interrupted by keyboard. Closing connection.")
            client_socket.close()

    def main(self):
        # Create the view
        # Start thread for capturing frames
        camera_thread = threading.Thread(target=self.get_capture)
        camera_thread.daemon = True
        camera_thread.start()

        self.master.mainloop()  # TODO FAR PARTIRE CON THREAD

    def signup_button_handler(self):
        name = self.textfield_view.get_text()
        with shared_frame:
            img = copy.deepcopy(actual_frame)
        if name != '':
            self._user_recognizer.register_user(name, img)
            new_user = User(name,
                            SeatComfortController.AWAKE_POSITION_DEFAULT,
                            SeatComfortController.SLEEPING_POSITION_DEFAULT)
            self._users.append(new_user)


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
