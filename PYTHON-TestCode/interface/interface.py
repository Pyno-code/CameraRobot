

import time
from tkinter import ttk
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.leftpannel.leftframe import LeftFrame
from interface.rightpannel.rightframe import RightFrame
import tkinter as tk
import asyncio
import data.variable

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # setup
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


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

        data.variable.logger = self.right_frame.main_frame.command_interface
    
    async def loop(self):
        data.variable.logger.log(data.variable.INFO, "Application started")
        self.update()

    def on_closing(self):
        data.variable.running = False
        list_task = asyncio.all_tasks(self.loop)
        print(list_task)
        time.sleep(3)
        try:
            for task in list_task:
                task.cancel()
        except:
            pass
        self.destroy()

        

