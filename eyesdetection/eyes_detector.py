import time
import copy
from datetime import datetime
from threading import Thread
from eyesdetection.eyes_detection import EyesDetection
from mooddetection.mood_detector import MoodDetector
from seatcomfortlogic.seat_comfort_controller import shared_frame_lock, actual_frame, user_lock, logged_user, stop_flag


class EyesDetector(Thread):
    def __init__(self, frequency, num_cons_frame, controller):
        super(EyesDetector, self).__init__()
        self.eyes_detection = EyesDetection()
        self.frequency = frequency
        self.num_cons_frame = num_cons_frame
        self.controller = controller

    def run(self):
        """
        Thread that handles the eyes detector, with a certain frequency look the frame
        and checks for a certain number of frames closed or open eyes are detected
        """
        # 1) while true + sleep(frequency)
        act_cons_frame = 1
        prev_detection = None
        while not stop_flag:
            time.sleep(1/self.frequency)
            # 2) took the actual frame (lock)
            with shared_frame_lock:
                actual_frame_cp = copy.deepcopy(actual_frame)
            # 3) classify the frame
            current_detection = self.detect_eyes(actual_frame_cp)

            # increment the number of actual consecutive frame only if the actual detection
            # is different from the previous state and the detection is equal to the previous
            with user_lock:
                actual_state = logged_user.get_mode()
            if actual_state != current_detection and prev_detection == current_detection:
                act_cons_frame += 1
            else:
                act_cons_frame = 1

            if act_cons_frame >= self.num_cons_frame:
                act_cons_frame = 1
                # 4) if for num_consecutive_frame you have detected closed eyes
                if current_detection:
                    # 4.1) put the seat in the preferred position for sleeping
                    with user_lock:
                        position = logged_user.get_sleeping_position()
                        logged_user.set_mode(True)
                    self.controller.rotate_back_seat(position, True)
                    # 4.2) print on the log the message
                    self.controller.add_log_message(f"eyes_detector - - [{datetime.now()}]: sleeping position set")
                # 5) if for num_consecutive_frame you have detected open eyes
                else:
                    # 5.1) put the seat in the preferred position for working
                    with user_lock:
                        position = logged_user.get_awake_position()
                        logged_user.set_mode(False)
                    self.controller.rotate_back_seat(position, True)
                    # 5.2) print on the log the message
                    self.controller.add_log_message(f"eyes_detector - - [{datetime.now()}]: awake position set")

                # 6) start the mood detector thread, that checks if the user liked the changed position
                #    and eventually restore the previous one
                with user_lock:
                    actual_state = logged_user.get_mode()
                mood_detector = MoodDetector(5, 1, self.controller, actual_state)
                mood_detector.start()
                mood_detector.join()

            prev_detection = current_detection

    def detect_eyes(self, img):
        return self.eyes_detection.classify_eyes(img)
