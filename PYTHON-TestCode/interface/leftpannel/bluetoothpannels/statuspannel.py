import tkinter as tk
from bluetooth_connection.constants import *

class BluetoothStatusPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for status panel
        status_label = tk.Label(self, text="Status Panel (Bluetooth)")
        status_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Add more widgets as needed
        label_working = tk.Label(self, text="BLUETOOTH CONNECTED : ")
        label_working.grid(row=1, column=0, padx=20, pady=5)

        label_working = tk.Label(self, text="WORKING : ")
        label_working.grid(row=2, column=0, padx=20, pady=5)

        


        # values
        self.label_bluetooth_value = tk.Label(self, text="false")
        self.label_bluetooth_value.grid(row=1, column=1, padx=20, pady=5)

        self.label_working_value = tk.Label(self, text="false")
        self.label_working_value.grid(row=2, column=1, padx=20, pady=5)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


    def loop(self, shared_dict):
        self.label_working_value.config(text=shared_dict[WORKING_STATUS_UUID])
        self.label_bluetooth_value.config(text=shared_dict["BLUETOOTH_CONNECTED"])
        # self.label_bluetooth_value.config(text=shared_dict[UUID])
