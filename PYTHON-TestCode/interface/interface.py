

from tkinter import ttk
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.leftpannel.leftframe import LeftFrame
from interface.rightpannel.rightframe import RightFrame
import tkinter as tk
import asyncio


class App(tk.Tk):
    def __init__(self, running, bluetooth_dict_values, bluetooth_order_dict, queue_logger, queue_recv_tcp_message, queue_send_tcp_message, queue_send_command, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # setup


        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.running = running


        self.bluetooth_dict_values = bluetooth_dict_values
        self.bluetooth_order_dict = bluetooth_order_dict
        self.queue_recv_tcp_message = queue_recv_tcp_message
        self.queue_send_tcp_message = queue_send_tcp_message
        self.queue_send_command = queue_send_command
        self.queue_logger = queue_logger

        self.title("CameraRobot")
        self.geometry("1080x720")  # Set initial size of the window

        # Configure the grid to allow responsive resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self.left_frame = LeftFrame(self, self.bluetooth_dict_values, self.bluetooth_order_dict)
        self.right_frame = RightFrame(self, self.queue_recv_tcp_message, self.queue_send_command)

        # Create a separator
        self.separator = ttk.Separator(self, orient='vertical')

        # Place frames and separator in the grid
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.separator.grid(row=0, column=1, sticky="ns")
        self.right_frame.grid(row=0, column=2, sticky="nsew")

        self.logger = self.right_frame.main_frame.command_interface
        self.update_video = self.right_frame.main_frame.camera_widget.update_video
        self.update_left_pannel = self.left_frame.loop

        self.queue_logger.put((self.logger.INFO,"Starting the application"))

        
        
    
    async def loop(self):
        while self.running.value:
            self.logger.log(self.queue_logger)
            self.update()
            await self.update_video()
            self.update_left_pannel(self.bluetooth_dict_values)
        self.destroy()
        

    def on_closing(self):
        self.running.value = False
    
    def start(self):
        asyncio.run(self.loop())

        

