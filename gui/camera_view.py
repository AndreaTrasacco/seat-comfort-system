import tkinter as tk
import numpy as np
from PIL import Image, ImageTk


class CameraView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        # create the window containing the camera frame
        self.image_label = tk.Label(self.frame, height=576, width=432, bg="white")
        self.frame.pack(side=tk.LEFT)
        self.image_label.pack()

        self.update_image(np.empty(shape=(576, 432, 3)))

    def update_image(self, img):
        """
        This method update the window with the frame inside img
        """
        image = Image.fromarray(img.astype("uint8"))
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo
