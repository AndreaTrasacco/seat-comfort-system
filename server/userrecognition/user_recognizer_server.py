import os

from deepface import DeepFace


class UserRecognizerServer:
    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"

    def detect_user(self, img):  # Returns the name of the user if it is registered, None otherwise
        lst = os.listdir(self._user_faces_dir)
        if len(lst) > 0:  # If there is at least one user registered
            recognition = DeepFace.find(img, db_path=self._user_faces_dir, enforce_detection=False)
            if recognition[0].empty:  # User not recognized
                return None
            else:  # User recognized
                file_name = os.path.basename(recognition[0]["identity"][0])
                name, extension = os.path.splitext(file_name)
                user_name = name.split("/")[-1]
                return user_name
        else:
            return None
