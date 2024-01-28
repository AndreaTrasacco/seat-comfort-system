import io
import time
import sys
import socket
import json

import numpy as np
from PIL import Image
from picamera import PiCamera


class ImagePicker:  # Flask server listening for GET requests for photos (captured at the moment of request)
    def __init__(self):
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.resolution = (540, 960)
        self._camera.capture("img.jpg", format="jpeg")

    def capture_image(self):  # Capture the image and returns it as a numpy array
        img = io.BytesIO()
        self._camera.capture(img, format="jpeg")
        img_pil = Image.open(img)
        return np.array(img_pil)

    def main(self):
        # Server configuration
        host = '169.254.101.5'
        port = 8000

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)

        print(f"Server listening on {host}:{port}")
        try:
            while True:
                # Accept a connection from a client
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")

                try:
                    while True:
                        # Receive data from the client
                        data = client_socket.recv(1024).decode()
                        # received_data = json.loads(data)

                        # Serialize the NumPy array
                        serialized_data = self.capture_image().tobytes()

                        # Send the actual serialized data
                        client_socket.sendall(serialized_data)
                except (ConnectionResetError, BrokenPipeError):
                    print("Client disconnected")
                    client_socket.close()

        except KeyboardInterrupt:
            print("Server interrupted by keyboard. Closing connection.")
            client_socket.close()
            server_socket.close()


if __name__ == '__main__':
    ImagePicker().main()
