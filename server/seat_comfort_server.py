import pickle
import socket
import os

import numpy as np
from PIL import Image
from deepface import DeepFace

import socket_communication
from server.eyesdetection.eyes_detection import EyesDetection
from server.users_storage_controller import UsersStorageController
from user import User


class SeatComfortServer:
    AWAKE_POSITION_DEFAULT = 0  # Position of the back seat when the user is awake
    SLEEPING_POSITION_DEFAULT = 60  # Degrees w.r.t "awake position" of the back seat when the user is sleeping

    def __init__(self):
        self._user_faces_dir = "data/user_faces_db"
        self._users_storage_controller = UsersStorageController()
        self._host = '169.254.232.238'
        self._port = 8000

        # TODO cancellare
        #self.user_recognizer_server = UserRecognizerServer()
        #self.mood_detector_server = MoodDetectorServer()
        self.eyes_detection = EyesDetection()

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

    def get_mood(self, img):  # It returns 1 if the detected emotion was "bad", 0 otherwise
        detection = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        emotion = detection[0]['dominant_emotion']
        return emotion

    def run(self):
        # create the socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self._host, self._port))
        server_socket.listen(1)

        print(f"Server listening on {self._host}:{self._port}")

        try:
            while True:
                # Accept a connection from a client
                socket_communication.sock, client_address = server_socket.accept()
                print(f"Connection from {client_address}")

                try:
                    while True:
                        data = socket_communication.recv()
                        if data['type'] == 'sign-up':
                            # save the recv name and image
                            name = data['name']
                            picture = np.frombuffer(data['picture'], dtype=np.uint8).reshape((540, 432, 3))
                            img_pil = Image.fromarray(picture)
                            img_pil.save(self._user_faces_dir + "/" + name + ".jpg")
                            new_user = User(name,
                                            SeatComfortServer.AWAKE_POSITION_DEFAULT,
                                            SeatComfortServer.SLEEPING_POSITION_DEFAULT)
                            self._users_storage_controller.save_user(new_user)

                            # create the reply
                            reply_msg = {'payload': 0}
                            socket_communication.send(reply_msg)
                            pass
                        elif data['type'] == 'user-recognition':
                            # recv the frame from the client
                            frame = np.frombuffer(data['frame'], dtype=np.uint8).reshape((540, 432, 3))
                            name = self.detect_user(frame)
                            # reply with the name of the detetcted user
                            if name is None:
                                reply_msg = {'payload': None}
                            else:
                                user = self._users_storage_controller.retrieve_user(name)
                                reply_msg = {'payload': pickle.dumps(user)}
                            socket_communication.send(reply_msg, "U")
                        elif data['type'] == 'need-detection':
                            # recv the frame from the client and classify the eyes state
                            frame = np.frombuffer(data['frame'], dtype=np.uint8).reshape((540, 432, 3))
                            eyes_state = self.eyes_detection.classify_eyes(frame)
                            reply_msg = {'payload': eyes_state}
                            socket_communication.send(reply_msg, "N")
                        elif data['type'] == 'mood-detection':
                            # recv the frame from the client and classify the emotion
                            frame = np.frombuffer(data['frame'], dtype=np.uint8).reshape((540, 432, 3))
                            emotion = self.get_mood(frame)
                            # reply with the detetcted emotion
                            reply_msg = {'payload': emotion}
                            socket_communication.send(reply_msg, "M")
                        elif data['type'] == 'save':
                            # recv the user to be saved
                            user = pickle.loads(data['user'])
                            self._users_storage_controller.save_user(user)
                            reply_msg = {'payload': 'OK'}
                            socket_communication.send(reply_msg)
                            print("Client disconnected")
                            socket_communication.sock.close()
                            break

                except (ConnectionResetError, BrokenPipeError):
                    print("Client disconnected")
                    socket_communication.sock.close()

        except KeyboardInterrupt:
            print("Client interrupted by keyboard. Closing connection.")
            socket_communication.sock.close()
            server_socket.close()


if __name__ == '__main__':
    SeatComfortServer().run()
