import tkinter as tk

from interface.utils.toggleswitch import ToggleSwitch
from bluetooth_connection.constants import *

class WifiCommandPannel(tk.Frame):

    def __init__(self, parent, value_dict, order_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (WiFi)")
        command_label.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
        # Add more widgets as needed
    

        self.label_ssid_connection = tk.Label(self, text="SSID : ")
        self.label_ssid_connection.grid(row=1, column=0, padx=20, pady=5)

        self.label_ssid_connection = tk.Label(self, text="PASSWORD : ")
        self.label_ssid_connection.grid(row=2, column=0, padx=20, pady=5)

        self.label_order_wifi_connection = tk.Label(self, text="ORDER WIFI CONNECTION : ")
        self.label_order_wifi_connection.grid(row=3, column=0, padx=20, pady=5)

        self.label_order_working_tcp = tk.Label(self, text="ORDER TCP CONNECTION : ")
        self.label_order_working_tcp.grid(row=4, column=0, padx=20, pady=5)

        self.label_order_tcp_connection = tk.Label(self, text="CONNECT TO THE SERVER TCP : ")
        self.label_order_tcp_connection.grid(row=5, column=0, padx=20, pady=5)

        self.label_order_update_tcp_connection = tk.Label(self, text="UPDATE TCP CONNECTION : ")
        self.label_order_update_tcp_connection.grid(row=6, column=0, padx=20, pady=5)


        # Add toggle switch



        entry_ssid = tk.Entry(self)
        entry_ssid.grid(row=1, column=1, padx=30, pady=5, sticky="nsew")
        entry_ssid.bind("<Return>", lambda x: value_dict.update({SSID_UUID: entry_ssid.get()}))

        entry_password = tk.Entry(self, show="*")
        entry_password.grid(row=2, column=1, padx=30, pady=5, sticky="nsew")
        entry_password.bind("<Return>", lambda x: value_dict.update({PASSWORD_UUID: entry_password.get()}))

        toggle_switch_order_wifi_connection = ToggleSwitch(self)
        toggle_switch_order_wifi_connection.func = lambda: value_dict.update({ORDER_WIFI_CONNECTION_UUID: "true" if toggle_switch_order_wifi_connection.get_state() else "false"})
        toggle_switch_order_wifi_connection.grid(row=3, column=1, padx=30, pady=5, sticky="nsew")

        toggle_switch_order_tcp_connection = ToggleSwitch(self)
        toggle_switch_order_tcp_connection.func = lambda: value_dict.update({ORDER_TCP_CONNECTION_UUID: "true" if toggle_switch_order_tcp_connection.get_state() else "false"})
        toggle_switch_order_tcp_connection.grid(row=4, column=1, padx=30, pady=5, sticky='nsew')

        toggle_switch_order_tcp_connection_to_server = ToggleSwitch(self)
        toggle_switch_order_tcp_connection_to_server.func = lambda: order_dict.update({"TCP_CONNECTION": "true" if toggle_switch_order_tcp_connection_to_server.get_state() else "false"})
        toggle_switch_order_tcp_connection_to_server.grid(row=5, column=1, padx=30, pady=5, sticky='nsew')

        toggle_switch_order_tcp_update = ToggleSwitch(self)
        toggle_switch_order_tcp_update.func = lambda: order_dict.update({"TCP_UPDATE": "true" if toggle_switch_order_tcp_update.get_state() else "false"})
        toggle_switch_order_tcp_update.grid(row=6, column=1, padx=30, pady=5, sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
    

    def return_entry_ssid(self, event):
        return self.entry_ssid.get()
    
    

