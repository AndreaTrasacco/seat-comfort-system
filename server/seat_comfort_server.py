import pickle
import socket

import numpy as np
from PIL import Image

import socket_communication
from server.eyesdetection.eyes_detection import EyesDetection
from server.mooddetection.mood_detector_server import MoodDetectorServer
from server.seatcomfortlogic.users_storage_controller import UsersStorageController
from server.userrecognition.user_recognizer_server import UserRecognizerServer
from user import User


class SeatComfortServer:
    AWAKE_POSITION_DEFAULT = 0  # Position of the back seat when the user is awake
    SLEEPING_POSITION_DEFAULT = 60  # Degrees w.r.t "awake position" of the back seat when the user is sleeping

    def __init__(self):
        self._user_faces_dir = "data/user_faces_db"
        self._users_storage_controller = UsersStorageController()
        self._host = '169.254.232.238'
        self._port = 8000

        self.user_recognizer_server = UserRecognizerServer()
        self.mood_detector_server = MoodDetectorServer()
        self.eyes_detection = EyesDetection()

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
                            name = self.user_recognizer_server.detect_user(frame)
                            # reply with the name of the detetcted user
                            if name is None:
                                reply_msg = {'payload': None}
                            else:
                                user = self._users_storage_controller.retrieve_user(name)
                                reply_msg = {'payload': pickle.dumps(user)}
                            socket_communication.send(reply_msg)
                        elif data['type'] == 'need-detection':
                            # recv the frame from the client and classify the eyes state
                            frame = np.frombuffer(data['frame'], dtype=np.uint8).reshape((540, 432, 3))
                            eyes_state = self.eyes_detection.classify_eyes(frame)
                            reply_msg = {'payload': eyes_state}
                            socket_communication.send(reply_msg)
                        elif data['type'] == 'mood-detection':
                            # recv the frame from the client and classify the emotion
                            frame = np.frombuffer(data['frame'], dtype=np.uint8).reshape((540, 432, 3))
                            emotion = self.mood_detector_server.get_mood(frame)
                            # reply with the detetcted emotion
                            reply_msg = {'payload': emotion}
                            socket_communication.send(reply_msg)
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
