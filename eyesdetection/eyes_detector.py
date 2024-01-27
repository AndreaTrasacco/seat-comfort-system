import time
import copy
from threading import Thread
from eyesdetection.eyes_detection import EyesDetection
from seatcomfortlogic.seat_comfort_controller import shared_frame_lock, actual_frame


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
        # TODO per recuperare il frame creare una copia, l'assegnamento è solo un riferimento
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

                #   4.2) TODO remember to do the change in mutual exclusion
                #   4.3) get the lock of the log
                #   4.4) print on the log the message
        # 5) if for num_consecutive_frame you have detected open eyes
                if closed_eyes == False:
        #       5.1) put the seat in the preferred position for working
        #       5.2) TODO remember to do the change in mutual exclusion
        #       5.3) get the lock of the log
        #       5.4) print on the log the message
            self.prev_detection = closed_eyes

    def detect_eyes(self, img):
        return self.eyes_detection.classify_eyes(img)
