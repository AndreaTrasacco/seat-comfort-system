from eyesdetection.eyes_detection import EyesDetection

class EyesDetector:
    def __init__(self):
        self.eyes_detection = EyesDetection()

    def detect_eyes(self, img):
        return self.eyes_detection.classify_eyes(img)
