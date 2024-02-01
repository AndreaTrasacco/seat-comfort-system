from deepface import DeepFace

# TODO cancellare classe
class MoodDetectorServer:

    def get_mood(self, img):  # It returns 1 if the detected emotion was "bad", 0 otherwise
        detection = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        emotion = detection[0]['dominant_emotion']
        return emotion
