import tkinter as tk
from tkinter import ttk
from leftpannel.selector import Selector
from leftpannel.bluetoothpannels.commandpannel import BluetoothCommandPannel
from leftpannel.bluetoothpannels.statuspannel import BluetoothStatusPannel
from leftpannel.motorspannels.commandpannel import MotorsCommandPannel
from leftpannel.motorspannels.statuspannel import MotorsStatusPannel
from leftpannel.wifipannels.commandpannel import WifiCommandPannel
from leftpannel.wifipannels.statuspannel import WifiStatusPannel
class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Create the Selector widget
        self.selector = Selector(self)
        self.selector.grid(row=0, column=0, sticky="nsew")

        # Create the Separator
        self.separator1 = ttk.Separator(self, orient='horizontal')
        self.separator1.grid(row=1, column=0, sticky="ew", pady=1)

        # Create the StatusPannel and CommandPannel initially with Wifi
        self.status_pannel = WifiStatusPannel(self)
        self.status_pannel.grid(row=2, column=0, sticky="nsew")

        self.separator2 = ttk.Separator(self, orient='horizontal')
        self.separator2.grid(row=3, column=0, sticky="ew", pady=1)

        self.command_pannel = WifiCommandPannel(self)
        self.command_pannel.grid(row=4, column=0, sticky="nsew")

        # Configure grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)  # Selector
        self.grid_rowconfigure(1, weight=0)  # Separator
        self.grid_rowconfigure(2, weight=5)  # StatusPannel
        self.grid_rowconfigure(3, weight=0)  # Separator
        self.grid_rowconfigure(4, weight=6)  # CommandPannel
        self.grid_columnconfigure(0, weight=1)

        # Initialize with Wifi panneaux
        self.update_pannels("Bluetooth")

    def update_pannels(self, status):
        # Update StatusPannel and CommandPannel based on status
        self.status_pannel.grid_forget()
        self.command_pannel.grid_forget()

        if status == "Bluetooth":
            self.status_pannel = BluetoothStatusPannel(self)
            self.command_pannel = BluetoothCommandPannel(self)
        elif status == "Motors":
            self.status_pannel = MotorsStatusPannel(self)
            self.command_pannel = MotorsCommandPannel(self)
        elif status == "Wifi":
            self.status_pannel = WifiStatusPannel(self)
            self.command_pannel = WifiCommandPannel(self)

        self.status_pannel.grid(row=2, column=0, sticky="nsew")
        self.command_pannel.grid(row=4, column=0, sticky="nsew")

        
# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    left_frame = LeftFrame(root)
    left_frame.pack(fill="both", expand=True)
    root.mainloop()
