import tkinter as tk


class LogView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.log_text = tk.Text(self.frame, height=10, width=70)
        self.scrollbar = tk.Scrollbar(self.frame, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=self.scrollbar.set, state='disabled', font=("Helvetica", 10))

        self.frame.pack(side=tk.BOTTOM, padx=10, pady=20)
        self.log_text.pack(side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def add_message(self, message):
        """
        Method used to add a new message in the log text field
        """
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.yview(tk.END)
        self.log_text.configure(state='disabled')
