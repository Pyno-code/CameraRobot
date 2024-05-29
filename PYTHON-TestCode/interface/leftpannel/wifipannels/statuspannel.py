import tkinter as tk
from bluetooth_connection.constants import *

class WifiStatusPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually       

        status_label = tk.Label(self, text="Status Panel (WiFi)")
        status_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Add more widgets as needed
        self.label_mac_address = tk.Label(self, text="MAC : ")
        self.label_mac_address.grid(row=1, column=0, padx=20, pady=5)

        self.label_ip = tk.Label(self, text="IP : ")
        self.label_ip.grid(row=2, column=0, padx=20, pady=5)

        self.label_port = tk.Label(self, text="PORT : ")
        self.label_port.grid(row=3, column=0, padx=20, pady=5)

        self.label_ssid = tk.Label(self, text="SSID : ")
        self.label_ssid.grid(row=4, column=0, padx=20, pady=5)

        self.label_password = tk.Label(self, text="PASSWORD : ")
        self.label_password.grid(row=5, column=0, padx=20, pady=5)


        self.label_wifi = tk.Label(self, text="WIFI CONNECTED :")
        self.label_wifi.grid(row=6, column=0, padx=20, pady=5)

        self.label_server_tcp = tk.Label(self, text="SERVER TCP ACTIVATED :")
        self.label_server_tcp.grid(row=7, column=0, padx=20, pady=5)


        # values
        self.label_mac_value = tk.Label(self, text="XX:XX:XX:XX:XX:XX")
        self.label_mac_value.grid(row=1, column=1, padx=20, pady=5)

        self.label_ip_value = tk.Label(self, text="192.168.0.4")
        self.label_ip_value.grid(row=2, column=1, padx=20, pady=5)

        self.label_port_value = tk.Label(self, text="5000")
        self.label_port_value.grid(row=3, column=1, padx=20, pady=5)

        self.label_ssid_value = tk.Label(self, text="test")
        self.label_ssid_value.grid(row=4, column=1, padx=20, pady=5)

        self.password_button = tk.Button(self, text="*********")
        self.password_button.grid(row=5, column=1, padx=20, pady=5)

        self.password_button.bind("<Button>", self.button_pressed)
        self.password_button.bind("<ButtonRelease>", self.button_unpressed)

        self.label_wifi_value = tk.Label(self, text="false")
        self.label_wifi_value.grid(row=6, column=1, padx=20, pady=5)

        self.label_server_tcp_value = tk.Label(self, text="false")
        self.label_server_tcp_value.grid(row=7, column=1, padx=20, pady=5)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    
    def button_pressed(self, event):
        self.password_button.config(text=self.shared_dict[PASSWORD_UUID])

    def button_unpressed(self, event):
        self.password_button.config(text="*********")
    
    def loop(self, shared_dict):
        self.shared_dict = shared_dict
        
        self.label_mac_value.config(text=shared_dict[ADDRESS_MAC_UUID])
        self.label_ip_value.config(text=shared_dict[IP_UUID])
        self.label_port_value.config(text=shared_dict[PORT_UUID])
        self.label_ssid_value.config(text=shared_dict[SSID_UUID])
        self.label_wifi_value.config(text=shared_dict[WIFI_STATUS_UUID])
        self.label_server_tcp_value.config(text=shared_dict[SERVER_TCP_STATUS_UUID])
        

