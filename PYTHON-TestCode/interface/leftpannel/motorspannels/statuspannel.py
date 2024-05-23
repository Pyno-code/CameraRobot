import tkinter as tk

class MotorsStatusPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for status panel
        status_label = tk.Label(self, text="Status Panel (Motors)")
        status_label.pack()
        # Add more widgets as needed
