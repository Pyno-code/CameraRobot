import tkinter as tk

class MotorsCommandPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (Motors)")
        command_label.pack()
        # Add more widgets as needed
