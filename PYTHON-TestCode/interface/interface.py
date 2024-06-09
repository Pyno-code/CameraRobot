

from threading import Thread
from tkinter import ttk
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.leftpannel.leftframe import LeftFrame
from interface.rightpannel.rightframe import RightFrame
import tkinter as tk
import asyncio
from interface.gamepad import Gamepad


class App(tk.Tk):
    def __init__(self, running, bluetooth_dict_values, bluetooth_order_dict, queue_logger, queue_recv_tcp_message, queue_send_tcp_message, queue_send_command, key_dict_handler, key_state_handler_value, *args, **kwargs):
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

        self.key_state_handler_value = key_state_handler_value
        self.key_dict_handler = key_dict_handler
        self.key_dict_handler["a"] = False
        self.key_dict_handler["z"] = False
        self.key_dict_handler["e"] = False
        self.key_dict_handler["s"] = False
        self.key_dict_handler["p"] = False
        self.key_dict_handler["m"] = False

        self.gamepad_controller = Gamepad()

        self.title("CameraRobot")
        self.geometry("1080x720")  # Set initial size of the window

        # Configure the grid to allow responsive resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=4)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self.left_frame = LeftFrame(self, self.bluetooth_dict_values, self.bluetooth_order_dict, self.queue_send_command, self.key_state_handler_value)
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

        self.bind("<KeyPress>", self.key_handler_press)
        self.bind("<KeyRelease>", self.key_handler_release)

        self.queue_logger.put((self.logger.INFO,"Starting the application"))

        
        
    
    async def loop(self):
        thread_gamepad = Thread(target=self.gamepad_controller.loop)
        thread_gamepad.start()
        while self.running.value:
            self.logger.log(self.queue_logger)
            self.update()
            if self.key_state_handler_value.value and not thread_gamepad.is_alive():
                thread_gamepad = Thread(target=self.gamepad_controller.loop)
                thread_gamepad.start()

            if self.gamepad_controller.updated:
                self.gamepad_handler()
            await self.update_video()
            self.update_left_pannel(self.bluetooth_dict_values)
        self.destroy()

    def gamepad_handler(self):
        if self.key_state_handler_value.value:
            if self.gamepad_controller.trigger_dict["TRIG_Z"] != 0:
                self.queue_send_command.put(f"MOTOR START _ BASE {self.gamepad_controller.trigger_dict['TRIG_Z']}")
            else:
                self.queue_send_command.put("MOTOR STOP _ BASE")
            if self.gamepad_controller.trigger_dict["ABS_X"] != 0:
                self.queue_send_command.put(f"MOTOR START _ MIDDLE {self.gamepad_controller.trigger_dict['ABS_X']}")
            else:
                self.queue_send_command.put("MOTOR STOP _ MIDDLE")
            if self.gamepad_controller.trigger_dict["ABS_RX"] != 0:
                self.queue_send_command.put(f"MOTOR START _ TOP {self.gamepad_controller.trigger_dict['ABS_RX']}")
                print(f"MOTOR START _ TOP {self.gamepad_controller.trigger_dict['ABS_RX']}")
            else:
                self.queue_send_command.put("MOTOR STOP _ TOP")
            print(self.gamepad_controller.trigger_dict)
            

    def key_handler_press(self, event):
        if self.key_state_handler_value.value:
            if event.char in self.key_dict_handler.keys() and not self.key_dict_handler[event.char]:
                print("key pressed : " , event.char)
                self.key_dict_handler[event.char] = True


                if event.char == "a":
                    self.queue_send_command.put("MOTOR START _ BASE 1")
                elif event.char == "z":
                    self.queue_send_command.put("MOTOR START _ MIDDLE 1")
                elif event.char == "p":
                    self.queue_send_command.put("MOTOR START _ TOP 1")
                elif event.char == "e":
                    self.queue_send_command.put("MOTOR START _ BASE -1")
                elif event.char == "s":
                    self.queue_send_command.put("MOTOR START _ MIDDLE -1")
                elif event.char == "m":
                    self.queue_send_command.put("MOTOR START _ TOP -1")
    
    def key_handler_release(self, event):
        if self.key_state_handler_value.value:
            if event.char in self.key_dict_handler.keys() and self.key_dict_handler[event.char]:
                print("key released : " , event.char)
                self.key_dict_handler[event.char] = False
                if event.char == "a":
                    self.queue_send_command.put("MOTOR STOP _ BASE")
                elif event.char == "z":
                    self.queue_send_command.put("MOTOR STOP _ MIDDLE")
                elif event.char == "p":
                    self.queue_send_command.put("MOTOR STOP _ TOP")
                elif event.char == "e":
                    self.queue_send_command.put("MOTOR STOP _ BASE")
                elif event.char == "s":
                    self.queue_send_command.put("MOTOR STOP _ MIDDLE")
                elif event.char == "m":
                    self.queue_send_command.put("MOTOR STOP _ TOP")
        

    def on_closing(self):
        self.running.value = False
    
    def start(self):
        asyncio.run(self.loop())

        

