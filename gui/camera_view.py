import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class CameraView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.image_label = tk.Label(self.frame, height=576, width=432, bg="white")
        self.frame.pack(side=tk.LEFT)
        self.image_label.pack()

        self.update_image(np.empty(shape=(960, 540, 3)))

    def update_image(self, img):
        image = Image.fromarray(img.astype("uint8"))
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
