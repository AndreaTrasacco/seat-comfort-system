import tkinter as tk

from gui.camera_view import CameraView
from gui.log_view import LogView
from gui.rigth_side_view import RightSideView
from gui.seat_view import SeatView
from gui.textfield_view import TextFieldView


class GUI:
    def __init__(self, master):
        self.master = master
        self.textfield_view = TextFieldView(self.master)
        self.camera_view = CameraView(self.master)
        self.right_side_view = RightSideView(self.master)


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
