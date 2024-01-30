import threading

from client.seatcomfortlogic.seat_comfort_controller import SeatComfortController

# lock to ensure mutual exclusion for the access of the frame
shared_frame_lock = threading.Lock()
actual_frame = None

# actual logged user
user_lock = threading.Lock()
logged_user = None

# lock for the seat position
seat_position_lock = threading.Lock()

# lock for the log
log_lock = threading.Lock()

# Flag to stop Threads
stop_flag: bool = False

controller = SeatComfortController()
