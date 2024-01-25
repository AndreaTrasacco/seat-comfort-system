import os

from deepface import DeepFace


class UserRecognitionManager:
    def __init__(self):
        self._user_faces_dir = "../data/user_faces_db"

    def register_user(self, name):  # TODO PASS ALSO THE IMAGE AS ARG
        pass
        # TODO WRITE IMAGE IN DIR "name.jpg"

    def detect_user(self, img_path):  # Returns the name of the user if it is registered, None otherwise
        recognition = DeepFace.find(img_path=img_path, db_path=self._user_faces_dir)
        if recognition[0].empty:  # User not recognized
            return None
        else:  # User recognized
            file_name = os.path.basename(recognition[0]["identity"][0])
            name, extension = os.path.splitext(file_name)
            user_name = name.split("/")[-1]
            return user_name


manager = UserRecognitionManager()
img_path = "../data/user_faces_db/Andrea.jpg"
print(manager.detect_user(img_path=img_path))
