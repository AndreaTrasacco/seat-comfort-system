import tkinter as tk

class LogView():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.log_text = tk.Text(self.frame, height=10, width=70)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=self.scrollbar.set, state=tk.DISABLED)

        self.frame.pack(side=tk.BOTTOM, padx=10, pady=20)
        self.log_text.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)