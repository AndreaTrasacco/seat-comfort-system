import tkinter as tk


class TextFieldView():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.entry = tk.Entry(self.frame, width=50)
        self.button = tk.Button(self.frame, text="Sign Up", command=self.send_text)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        self.button.pack(side=tk.LEFT, padx=(5, 0))

        self.frame.pack(side=tk.TOP)

    def send_text(self):
        text = self.entry.get()
        # TODO codice per gestire l'invio del nome
