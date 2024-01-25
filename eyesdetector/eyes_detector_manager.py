from eyesdetector.eyes_detector import EyesDetector

class EyesDetectorManager:
    def __init__(self):
        self.eyes_detector = EyesDetector()

    def detect_eyes(self, image_path):
        """
        :param
            image_path: path to the image to be classified (as closed or open eyes)
        :return:
            True if the eyes are closed or False if the eyes are opened
        """
        return self.eyes_detector.image_demo(image_path)
