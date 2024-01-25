import tkinter as tk
from PIL import ImageTk, Image

class SeatView():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.seat = Image.open("img/seat.png")

        self.canvas = tk.Canvas(self.frame, width=300, height=300)
        self.canvas.pack()
        self.seat = self.seat.resize((300, 150))

        self.seat_tk = ImageTk.PhotoImage(self.seat)

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.seat_tk)

        self.left_arrow_image = Image.open("img/left_arrow.jpg")
        self.right_arrow_image = Image.open("img/right_arrow.jpg")
        self.left_arrow_photo = ImageTk.PhotoImage(self.left_arrow_image)
        self.right_arrow_photo = ImageTk.PhotoImage(self.right_arrow_image)

        self.left_arrow_label = tk.Label(self.frame, image=self.left_arrow_photo, cursor="hand2")
        self.left_arrow_label.pack(side=tk.LEFT)
        self.left_arrow_label.bind("<Button-1>", self.left_arrow_handler)

        self.right_arrow_label = tk.Label(self.frame, image=self.right_arrow_photo, cursor="hand2")
        self.right_arrow_label.pack(side=tk.RIGHT)
        self.right_arrow_label.bind("<Button-1>", self.right_arrow_handler)

        self.frame.pack(side=tk.TOP)

    def left_arrow_handler(self, event):
        # TODO logica della gestione della freccia sinistra
        pass

    def right_arrow_handler(self, event):
        # TODO logica della gestione della freccia destra
        pass