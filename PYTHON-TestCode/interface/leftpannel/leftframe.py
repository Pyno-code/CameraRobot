import tkinter as tk
from tkinter import ttk
from leftpannel.selector import Selector

class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.status = "Bluetooth"

        self.config(bg="white")  # Just to differentiate visually
        self.pack_propagate(False)   # Prevent frame from resizing to fit its content

        selector = Selector(self)
        selector.pack(side=tk.TOP, fill=tk.BOTH, expand=True)