import io
import time
from threading import Thread

import numpy as np
from PIL import Image
from picamera import PiCamera

import globals as glob


class ImagePicker(Thread):
    def __init__(self, frequency=100):
        super(ImagePicker, self).__init__()
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.hflip = True
        self._camera.resolution = (432, 540)
        self._frequency = frequency

    def capture_image(self):  # Capture the image and returns it as a numpy array
        img = io.BytesIO()
        self._camera.capture(img, format="jpeg")
        img_pil = Image.open(img)
        return np.array(img_pil)

    def run(self):
        while not glob.stop_flag:
            time.sleep(1/self._frequency)  # TODO TOGLIERE O MODIFICARE FREQUENCY
            image = self.capture_image()
            with glob.shared_frame_lock:
                glob.actual_frame = image
                if not glob.stop_flag:
                    glob.controller.update_camera(glob.actual_frame)
