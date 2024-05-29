import tkinter as tk
from interface.utils.toggleswitch import ToggleSwitch
from bluetooth_connection.constants import *

class BluetoothCommandPannel(tk.Frame):
    def __init__(self, parent, shared_dict_values, shared_dict_order, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (Bluetooth)")
        command_label.grid(row=0, column=0, columnspan=2, pady=20)
        # Add more widgets as needed

        self.label_bluetooth_connection = tk.Label(self, text="BLUETOOTH CONNECTION : ")
        self.label_bluetooth_connection.grid(row=1, column=0, padx=20, pady=5)

        self.label_bluetooth_update = tk.Label(self, text="BLUETOOTH UPDATE : ")
        self.label_bluetooth_update.grid(row=2, column=0, padx=20, pady=5)

        self.label_order_working = tk.Label(self, text="ACTIVATE ESP32 : ")
        self.label_order_working.grid(row=3, column=0, padx=20, pady=5)



        # Add toggle switch
        toggle_switch_bluetooth_connection = ToggleSwitch(self)
        toggle_switch_bluetooth_connection.func = lambda: shared_dict_order.update({"BLUETOOTH_CONNECTION": "true" if toggle_switch_bluetooth_connection.get_state() else "false"})
        toggle_switch_bluetooth_connection.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
        
        toggle_switch_bluetooth_update = ToggleSwitch(self)
        toggle_switch_bluetooth_update.func = lambda: shared_dict_order.update({"BLUETOOTH_UPDATE": "true" if toggle_switch_bluetooth_update.get_state() else "false"})
        toggle_switch_bluetooth_update.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

        toggle_switch_order_working = ToggleSwitch(self)
        toggle_switch_order_working.func = lambda: shared_dict_values.update({ORDER_WORKING_UUID: "true" if toggle_switch_order_working.get_state() else "false"})
        toggle_switch_order_working.grid(row=3, column=1, padx=30, pady=5, sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
    
