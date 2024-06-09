import tkinter as tk
from tkinter import ttk
from interface.leftpannel.selector import Selector
from interface.leftpannel.bluetoothpannels.commandpannel import BluetoothCommandPannel
from interface.leftpannel.bluetoothpannels.statuspannel import BluetoothStatusPannel
from interface.leftpannel.motorspannels.commandpannel import MotorsCommandPannel
from interface.leftpannel.motorspannels.statuspannel import MotorsStatusPannel
from interface.leftpannel.wifipannels.commandpannel import WifiCommandPannel
from interface.leftpannel.wifipannels.statuspannel import WifiStatusPannel
class LeftFrame(tk.Frame):
    def __init__(self, parent, shared_dict_values, shared_dict_order, queue_send_command, key_state_handler_value, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create the Selector widget
        self.selector = Selector(self)
        self.selector.grid(row=0, column=0, sticky="nsew")

        # Create the Separator
        self.separator1 = ttk.Separator(self, orient='horizontal')
        self.separator1.grid(row=1, column=0, sticky="ew", pady=1)


        self.separator2 = ttk.Separator(self, orient='horizontal')
        self.separator2.grid(row=3, column=0, sticky="ew", pady=1)


        self.status_pannel = tk.Frame(self)
        self.command_pannel = tk.Frame(self)

        # Configure grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)  # Selector
        self.grid_rowconfigure(1, weight=0)  # Separator
        self.grid_rowconfigure(2, weight=5)  # StatusPannel
        self.grid_rowconfigure(3, weight=0)  # Separator
        self.grid_rowconfigure(4, weight=6)  # CommandPannel
        self.grid_columnconfigure(0, weight=1)
        
        self.bluetooth_status_pannel = BluetoothStatusPannel(self)
        self.bluetooth_command_pannel = BluetoothCommandPannel(self, shared_dict_values, shared_dict_order)
        
        self.motor_status_pannel = MotorsStatusPannel(self, queue_send_command)
        self.motor_command_pannel = MotorsCommandPannel(self, queue_send_command, key_state_handler_value)

        self.wifi_status_pannel = WifiStatusPannel(self)
        self.wifi_command_pannel = WifiCommandPannel(self, shared_dict_values, shared_dict_order)

        # Initialize with Wifi panneaux
        self.status = "Bluetooth"
        self.update_pannels(self.status)

    def update_pannels(self, status):
        # Update StatusPannel and CommandPannel based on status
        self.status_pannel.grid_forget()
        self.command_pannel.grid_forget()

        self.status = status

        if status == "Bluetooth":
            self.status_pannel = self.bluetooth_status_pannel
            self.command_pannel = self.bluetooth_command_pannel
        elif status == "Motors":
            self.status_pannel = self.motor_status_pannel
            self.command_pannel = self.motor_command_pannel
        elif status == "Wifi":
            self.status_pannel = self.wifi_status_pannel
            self.command_pannel = self.wifi_command_pannel

        self.status_pannel.grid(row=2, column=0, sticky="nsew")
        self.command_pannel.grid(row=4, column=0, sticky="nsew")

    def loop(self, shared_dict):
        if self.status == "Bluetooth" or self.status == "Wifi":
            self.status_pannel.loop(shared_dict)
        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    left_frame = LeftFrame(root)
    left_frame.pack(fill="both", expand=True)
    root.mainloop()
