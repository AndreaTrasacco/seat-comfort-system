import copy
import time
import IAProject.client.globals as glob
from threading import Thread

class MoodDetector(Thread):
    def __init__(self, tot_seconds, frequency, user_state):
        super(MoodDetector, self).__init__()
        self._bad_emotions = ["angry", "disgust", "sad", "fear"]
        self.tot_seconds = tot_seconds
        self.frequency = frequency
        self.user_state = user_state

    def get_mood(self, img):  # It returns 1 if the detected emotion was "bad", 0 otherwise
        # detection = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)
        # emotion = detection[0]['dominant_emotion']
        # TODO
        emotion = "happy"
        if emotion in self._bad_emotions:  # If the user didn't appreciate the change of seat position by system
            return emotion, 1
        return emotion, 0  # The user appreciated the change of seat position by system

    def run(self):
        """
        Thread that handles the mood detector, with a certain frequency look the frame
        and checks if the user doesn't like the changed position
        """
        # 1) while(tot_sec)
        act_seconds = 0
        while act_seconds < self.tot_seconds:
            time.sleep(1 / self.frequency)
            act_seconds += (1 / self.frequency)
            # 2) took the actual frame
            with glob.shared_frame_lock:
                actual_frame_cp = copy.deepcopy(glob.actual_frame)
            # 3) classify the frame
            emotion, class_emotion = self.get_mood(actual_frame_cp)
            # 4) print in the log the emotion detected
            glob.controller.add_log_message(f"MOOD DETECTOR - - {emotion} detected")
            # 5) if the detected emotion is a bad emotion
            if class_emotion == 1:
                # 5.1) restore the previous position
                if self.user_state:  # if user_state is True (seat is in sleep position) restore the awake position
                    with glob.user_lock:
                        glob.logged_user.set_mode(False)
                        position = glob.logged_user.get_position()
                        mode = "AWAKE"
                else:  # The user state is False (seat is in awake position) restore the sleep position
                    with glob.user_lock:
                        glob.logged_user.set_mode(True)
                        position = glob.logged_user.get_position()
                        mode = "SLEEP"
                glob.controller.rotate_back_seat(position, True)
                # 5.2) print in the log that the position is changed
                glob.controller.add_log_message(f"MOOD DETECTOR - - Previous position restored (" + mode + ")")
                return
