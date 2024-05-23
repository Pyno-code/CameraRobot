

from leftpannel.leftframe import LeftFrame
from rightpannel.rightframe import RightFrame
from tkinter import ttk
import tkinter as tk


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("CameraRobot")
        self.geometry("1080x720")  # Set initial size of the window

        # Configure the grid to allow responsive resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self.left_frame = LeftFrame(self)
        self.right_frame = RightFrame(self)

        # Create a separator
        self.separator = ttk.Separator(self, orient='vertical')

        # Place frames and separator in the grid
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.separator.grid(row=0, column=1, sticky="ns")
        self.right_frame.grid(row=0, column=2, sticky="nsew")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()