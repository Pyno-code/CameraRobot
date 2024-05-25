import tkinter as tk
from interface.utils.toggleswitch import ToggleSwitch

class BluetoothCommandPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (Bluetooth)")
        command_label.grid(row=0, column=0, columnspan=2, pady=20)
        # Add more widgets as needed

        self.label_order_working = tk.Label(self, text="ACTIVATE ESP32 : ")
        self.label_order_working.grid(row=1, column=0, padx=20, pady=5)

        self.label_order_wifi_connection = tk.Label(self, text="ORDER WIFI CONNECTION : ")
        self.label_order_wifi_connection.grid(row=2, column=0, padx=20, pady=5)

        # Add toggle switch
        
        toggle_switch_order_working = ToggleSwitch(self)
        toggle_switch_order_working.grid(row=1, column=1, padx=30, pady=5, sticky='nsew')

        toggle_switch_order_wifi_connection = ToggleSwitch(self)
        toggle_switch_order_wifi_connection.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)