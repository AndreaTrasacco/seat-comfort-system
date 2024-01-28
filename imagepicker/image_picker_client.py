import json
import socket
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
                # Send a message to the server
                message_to_send = {"message": "request_for_photo"}
                client_socket.send(json.dumps(message_to_send).encode())
                # Receive the actual image data
                image_data = b''
                while len(image_data) < 1555200:
                    data = client_socket.recv(1555200 - len(image_data))
                    if not data:
                        break  # Connection closed
                    image_data += data

                # Convert the received data to a numpy array
                image_np = np.frombuffer(image_data, dtype=np.uint8)
                # Reshape the NumPy array to the original image shape
                image = image_np.reshape((1920, 1080, 3))
                with glob.shared_frame_lock:
                    glob.actual_frame = image
                    if not glob.stop_flag:
                        glob.controller.update_camera(glob.actual_frame)

        except KeyboardInterrupt:
            print("Client interrupted by keyboard. Closing connection.")
            client_socket.close()
