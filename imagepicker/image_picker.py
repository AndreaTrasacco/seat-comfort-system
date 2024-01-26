import io
import time

import numpy as np
from PIL import Image
from flask import Flask
from flask_restful import Api
from picamera import PiCamera

app = Flask(__name__)
api = Api(app)


class ImagePicker:  # Flask server listening for GET requests for photos (captured at the moment of request)
    def __init__(self):
        self._camera = PiCamera()
        time.sleep(2)
        self._camera.resolution = (540, 960)

    def capture_image(self):  # Capture the image and returns it as a numpy array
        img = io.BytesIO()
        self._camera.capture(img, format="jpeg")
        img_pil = Image.open(img)
        return np.array(img_pil)

    def get(self):
        return {'photo': self.capture_image()}


api.add_resource(ImagePicker, '/Raspberry/photo')
if __name__ == '__main__':
    app.run(debug=True, host='169.254.101.5')
