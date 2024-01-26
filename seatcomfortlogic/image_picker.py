import io
import time

import numpy as np
from PIL import Image
from picamera import PiCamera


class ImagePicker:
    def __init__(self):
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.resolution = (1440,1920)

    def capture_image(self):  # Capture the image and returns it as a numpy array
        img = io.BytesIO()
        self._camera.capture(img, format="jpeg")
        img_pil = Image.open(img)
        return np.array(img_pil)
