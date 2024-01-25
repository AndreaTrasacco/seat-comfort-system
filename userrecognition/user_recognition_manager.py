import os

from PIL import Image
from deepface import DeepFace


class UserRecognitionManager:
    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"

    def register_user(self, name, img):
        img_pil = Image.fromarray(img)
        img_pil.save(self._user_faces_dir + "/" + name + ".jpg")

    def detect_user(self, img):  # Returns the name of the user if it is registered, None otherwise
        recognition = DeepFace.find(img, db_path=self._user_faces_dir)
        if recognition[0].empty:  # User not recognized
            return None
        else:  # User recognized
            file_name = os.path.basename(recognition[0]["identity"][0])
            name, extension = os.path.splitext(file_name)
            user_name = name.split("/")[-1]
            return user_name
