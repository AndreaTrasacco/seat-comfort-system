import json
import socket
import time
from threading import Thread

import numpy as np

import globals as glob


class ImagePickerClient(Thread):
    def run(self):
        # Server configuration
        host = '169.254.101.5'
        port = 8000

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))

        try:
            while not glob.stop_flag:
                time.sleep(0.01)  # TODO METTERE IN UNA COSTANTE
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
                with glob.shared_frame_lock:
                    glob.actual_frame = image
                    glob.controller.camera_view.update_image(glob.actual_frame)  # TODO METTERE IN CONTROLLER
                print("IMAGE PICKER")

        except KeyboardInterrupt:
            print("Client interrupted by keyboard. Closing connection.")
            client_socket.close()

# TODO GESTIRE CASO IN CUI L'UTENTE CLICCA X