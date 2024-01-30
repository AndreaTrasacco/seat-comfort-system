import time
import tkinter as tk

from PIL import ImageTk, Image

import globals as glob


class SeatView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master, bg="white")
        self.seat = Image.open("img/seat.png")
        self.back_seat = Image.open("img/back_seat_2.png")

        self.canvas = tk.Canvas(self.frame, width=600, height=350, bg="white")
        self.canvas.pack()

        # create the image related to the back seat
        self.back_seat = self.back_seat.resize((600, 300))
        self.back_seat_tk = ImageTk.PhotoImage(self.back_seat)
        self.canvas_back_seat = self.canvas.create_image(15, 350, anchor=tk.SW, image=self.back_seat_tk)
        self.actual_degree = 0

        # create the image related to the seat
        self.seat = self.seat.resize((150, 60))
        self.seat_tk = ImageTk.PhotoImage(self.seat)
        self.canvas.create_image(270, 315, anchor=tk.SW, image=self.seat_tk)

        # create the two arrows used to move the seat
        self.left_arrow_image = Image.open("img/left_arrow.jpg")
        self.right_arrow_image = Image.open("img/right_arrow.jpg")
        self.left_arrow_photo = ImageTk.PhotoImage(self.left_arrow_image)
        self.right_arrow_photo = ImageTk.PhotoImage(self.right_arrow_image)

        self.left_arrow_label = tk.Label(self.frame, image=self.left_arrow_photo, cursor="hand2")
        self.left_arrow_label.pack(side=tk.LEFT)

        self.right_arrow_label = tk.Label(self.frame, image=self.right_arrow_photo, cursor="hand2")
        self.right_arrow_label.pack(side=tk.RIGHT)

        self.left_arrow_label.configure(state="disabled")
        self.right_arrow_label.configure(state="disabled")

        self.frame.pack(side=tk.TOP)

    def rotate(self, degrees, absolute):
        if not absolute: # relative degrees
            self.actual_degree += degrees
        else: # absolute degree (progressive change of the seat, 10 degrees at a time)
            direction = 1
            if self.actual_degree < degrees:
                min = self.actual_degree
                max = degrees
            elif self.actual_degree > degrees:
                max = self.actual_degree
                min = degrees
                direction = -1
            for i in range(min, max, 10):
                self.rotate(10 * direction, False)
                time.sleep(0.5)
        rotated_image = self.back_seat.rotate(self.actual_degree, resample=Image.BICUBIC,
                                              center=((self.back_seat.width // 2) - 27, self.back_seat.height - 72))
        rotated_image_tk = ImageTk.PhotoImage(rotated_image)
        self.canvas.itemconfig(self.canvas_back_seat, image=rotated_image_tk)
        self.back_seat_tk = rotated_image_tk

    def change_button(self, status):
        if status:  # if status is True, able the clickable arrows
            self.left_arrow_label.configure(state="normal")
            self.left_arrow_label.bind("<Button-1>", glob.controller.left_arrow_handler)
            self.right_arrow_label.configure(state="normal")
            self.right_arrow_label.bind("<Button-1>", glob.controller.right_arrow_handler)
        else:  # if status is False, disable the clickable arrows
            self.left_arrow_label.configure(state="disabled")
            self.left_arrow_label.unbind("<Button-1>")
            self.right_arrow_label.configure(state="disabled")
            self.right_arrow_label.unbind("<Button-1>")
