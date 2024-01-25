import tkinter as tk
from PIL import Image, ImageTk


class CameraView():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.image_label = tk.Label(self.frame)
        self.frame.pack(side=tk.LEFT)
        self.image_label.pack()

        self.update_image("../data/closed_eyes.jpg")

    def update_image(self, image_path):
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
