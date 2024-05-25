import tkinter as tk

class WifiStatusPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually       

        status_label = tk.Label(self, text="Status Panel (WiFi)")
        status_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Add more widgets as needed
        label_mac_address = tk.Label(self, text="MAC : ")
        label_mac_address.grid(row=1, column=0, padx=20, pady=5)

        label_ip = tk.Label(self, text="IP : ")
        label_ip.grid(row=2, column=0, padx=20, pady=5)

        label_port = tk.Label(self, text="PORT : ")
        label_port.grid(row=3, column=0, padx=20, pady=5)

        label_ssid = tk.Label(self, text="SSID : ")
        label_ssid.grid(row=4, column=0, padx=20, pady=5)

        label_password = tk.Label(self, text="PASSWORD : ")
        label_password.grid(row=5, column=0, padx=20, pady=5)

        label_server_tcp = tk.Label(self, text="SERVER TCP ACTIVATED :")
        label_server_tcp.grid(row=6, column=0, padx=20, pady=5)

        label_server_connection_tcp = tk.Label(self, text="TCP CONNECTED :")
        label_server_connection_tcp.grid(row=7, column=0, padx=20, pady=5)


        # values
        label_mac_value = tk.Label(self, text="XX:XX:XX:XX:XX:XX")
        label_mac_value.grid(row=1, column=1, padx=20, pady=5)

        label_ip_value = tk.Label(self, text="192.168.0.4")
        label_ip_value.grid(row=2, column=1, padx=20, pady=5)

        label_port_value = tk.Label(self, text="5000")
        label_port_value.grid(row=3, column=1, padx=20, pady=5)

        label_ssid_value = tk.Label(self, text="test")
        label_ssid_value.grid(row=4, column=1, padx=20, pady=5)

        self.password_button = tk.Button(self, text="*********")
        self.password_button.grid(row=5, column=1, padx=20, pady=5)

        self.password_button.bind("<Button>", self.button_pressed)
        self.password_button.bind("<ButtonRelease>", self.button_unpressed)

        label_server_tcp_value = tk.Label(self, text="false")
        label_server_tcp_value.grid(row=6, column=1, padx=20, pady=5)

        label_server_connection_tcp_value = tk.Label(self, text="false")
        label_server_connection_tcp_value.grid(row=7, column=1, padx=20, pady=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    
    def button_pressed(self, event):
        self.password_button.config(text="password")

    def button_unpressed(self, event):
        self.password_button.config(text="*********")

        

