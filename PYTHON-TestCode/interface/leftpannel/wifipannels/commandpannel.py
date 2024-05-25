import tkinter as tk

from interface.utils.toggleswitch import ToggleSwitch

class WifiCommandPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (WiFi)")
        command_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
        # Add more widgets as needed

        self.label_order_working_tcp = tk.Label(self, text="ORDER TCP INITIALISATION : ")
        self.label_order_working_tcp.grid(row=1, column=0, padx=20, pady=5)

        self.label_order_tcp_connection = tk.Label(self, text="TCP CONNECTION : ")
        self.label_order_tcp_connection.grid(row=2, column=0, padx=20, pady=5)

        # Add toggle switch
        
        toggle_switch_order_working_tcp = ToggleSwitch(self)
        toggle_switch_order_working_tcp.grid(row=1, column=1, padx=30, pady=5, sticky='nsew')

        button_order_tcp_connection = tk.Button(self, text="CONNECT")
        button_order_tcp_connection.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
