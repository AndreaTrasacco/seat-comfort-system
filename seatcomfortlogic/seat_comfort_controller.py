from eyesdetector.eyes_detector import EyesDetector
from seatcomfortlogic.users_storage_controller import UsersStorageController


class SeatComfortController:
    def __init__(self):
        self._users_storage_controller = UsersStorageController()
        self._users = self._users_storage_controller.retrieve_users()
        self._need_detector = EyesDetector()

    def main(self):
        # Create the view

        # Start thread for capturing frames

        pass


'''
constant FRAME_FREQUENCY
--> PRINT EVERYTHING ON THE LOG TEXTAREA
Logic:
    1)  User Recognition: 
        [Whenever the new user clicks "Signup" button a frame is captured and the user is stored]
        Until user is not recognized
            Each frame is used as input to user recognition module
        Change the position of the seat to the preferred one for the user when he/she is awake
    2)  Need Detection:
        Until a *different* need is not detected (N consecutive frames of the same class)
            Each frame is used as input to eyes detection
        Change the position of the seat to the preferred one for the user (depending on the detected class)
    3)  Mood Detection:
        For M consecutive frames:
            If a "bad" emotion is detected, restore the position (??)
    Whenever the user changes the seat position manually --> store the new preferred position
'''
