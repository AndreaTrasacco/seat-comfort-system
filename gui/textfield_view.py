import tkinter as tk


class TextFieldView():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.entry = tk.Entry(self.frame)
        self.button = tk.Button(self.frame, text="Sign Up", command=self.send_text)
        self.frame.pack(side=tk.TOP)
        self.entry.pack(side=tk.LEFT)
        self.button.pack(side=tk.LEFT)

    def send_text(self):
        text = self.entry.get()
        # TODO codice per gestire l'invio del nome
