import copy
import time
from threading import Thread

import globals as glob
import socket_communication
from client.mooddetection.mood_detector import MoodDetector


class EyesDetector(Thread):
    def __init__(self, frequency, num_cons_frame):
        super(EyesDetector, self).__init__()
        self.frequency = frequency  # frequency of the detection
        self.num_cons_frame = num_cons_frame  # Number of consecutive frames to be used for changing class

    def run(self):
        """
        Thread that handles the eyes detector, with a certain frequency looks the frame
        and checks if for a certain number of frames closed or open eyes are detected
        """
        # 1) while true + sleep(frequency)
        act_cons_frame = 1
        prev_detection = None
        while not glob.stop_flag:
            time.sleep(1 / self.frequency)
            # 2) took the actual frame (lock)
            with glob.shared_frame_lock:
                actual_frame_cp = copy.deepcopy(glob.actual_frame)
            # 3) classify the frame
            socket_communication.send({"type": "need-detection", "frame": actual_frame_cp.tobytes()})
            current_detection = socket_communication.recv()["payload"]
            if current_detection == -1:  # No faces in front of the camera
                act_cons_frame = 1
                continue
            with glob.user_lock:
                actual_state = glob.logged_user.get_mode()
            # increment the number of actual consecutive frame only if the actual detection
            # is different from the actual state and the detection is equal to the previous one
            if actual_state != current_detection and prev_detection == current_detection:
                act_cons_frame += 1
            else:
                act_cons_frame = 1

            if act_cons_frame >= self.num_cons_frame:
                act_cons_frame = 1
                # 4) if for num_consecutive_frame you have detected closed eyes
                if current_detection == 1:
                    # 4.1) put the seat in the preferred position for sleeping
                    with glob.user_lock:
                        glob.logged_user.set_mode(True)
                        position = glob.logged_user.get_position()
                    glob.controller.rotate_back_seat(position, True)
                    # 4.2) print on the log the message
                    glob.controller.add_log_message(f"NEED DETECTOR - - SLEEP position set")
                # 5) if for num_consecutive_frame you have detected open eyes
                else:
                    # 5.1) put the seat in the preferred position for awakening
                    with glob.user_lock:
                        glob.logged_user.set_mode(False)
                        position = glob.logged_user.get_position()
                    glob.controller.rotate_back_seat(position, True)
                    # 5.2) print on the log the message
                    glob.controller.add_log_message(f"NEED DETECTOR - - AWAKE position set")

                # 6) start the mood detector thread, that checks if the user doesn't like
                #    the changed position and eventually restore the previous one
                with glob.user_lock:
                    actual_state = glob.logged_user.get_mode()
                mood_detector = MoodDetector(5, 1, actual_state)
                mood_detector.start()
                mood_detector.join()
            prev_detection = current_detection
