from deepface import DeepFace


class MoodDetector:
    def __init__(self):
        self._bad_emotions = ["angry", "disgust"]

    def get_mood(self, img):  # It returns 1 if the detected emotion was "bad", 0 otherwise
        detection = DeepFace.analyze(img, actions=["emotion"])
        emotion = detection[0]['dominant_emotion']
        if emotion in self._bad_emotions:  # If the user didn't appreciate the change of seat position by system
            return 1
        return 0  # The user appreciated the change of seat position by system
