import time
import copy
from datetime import datetime
from threading import Thread
from eyesdetection.eyes_detection import EyesDetection
from seatcomfortlogic.seat_comfort_controller import shared_frame_lock, actual_frame, user_lock, logged_user


class EyesDetector(Thread):
    def __init__(self, frequency, num_cons_frame, controller):
        super(EyesDetector, self).__init__()
        self.eyes_detection = EyesDetection()
        self.frequency = frequency
        self.num_cons_frame = num_cons_frame
        self.act_cons_frame = 0
        self.prev_detection = None
        self.controller = controller

    def run(self):
        """
        Thread who handles the eyes detector, with a certain frequency look the frame
        and checks for a certain number of frames closed or open eyes are detected
        :return:
        """
        # 1) while true + sleep(frequency)
        while True:
            time.sleep(1/self.frequency)
            # 2) took the actual frame (lock)
            with shared_frame_lock:
                actual_frame_cp = copy.deepcopy(actual_frame)
            # 3) classify the frame
            closed_eyes = self.detect_eyes(actual_frame_cp)

            if self.prev_detection == closed_eyes:
                self.act_cons_frame += 1
            else:
                self.act_cons_frame = 0

            if self.act_cons_frame >= self.num_cons_frame:
                # 4) if for num_consecutive_frame you have detected closed eyes
                if closed_eyes:
                    # 4.1) put the seat in the preferred position for sleeping
                    with user_lock:
                        self.controller.rotate_back_seat(logged_user.get_sleeping_position(), True)
                    # 4.2) print on the log the message
                    self.controller.add_log_message(f"eyes_detector - - [{datetime.now()}]: sleeping position set")
                # 5) if for num_consecutive_frame you have detected open eyes
                if not closed_eyes:
                    # 5.1) put the seat in the preferred position for working
                    with user_lock:
                        self.controller.rotate_back_seat(logged_user.get_awake_position(), True)
                    # 5.2) print on the log the message
                    self.controller.add_log_message(f"eyes_detector - - [{datetime.now()}]: awake position set")
            self.prev_detection = closed_eyes

    def detect_eyes(self, img):
        return self.eyes_detection.classify_eyes(img)
