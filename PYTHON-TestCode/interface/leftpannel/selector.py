import tkinter as tk
from tkinter import ttk

class Selector(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.status = "Bluetooth"

        # Create a frame for the buttons
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bluetooth_button = tk.Button(button_frame, text="Bluetooth", command=lambda: self.update_status("Bluetooth"))
        bluetooth_button.grid(row=0, column=1, sticky="nsew")

        wifi_button = tk.Button(button_frame, text="Wifi", command=lambda: self.update_status("Wifi"))
        wifi_button.grid(row=0, column=0, sticky="nsew")

        motors_button = tk.Button(button_frame, text="Motors", command=lambda: self.update_status("Motors"))
        motors_button.grid(row=0, column=2, sticky="nsew")

        # Add a separator below the buttons
        separator = ttk.Separator(button_frame, orient='horizontal')
        separator.grid(row=1, columnspan=3, sticky="ew", pady=1)

        # Add a label to display the clicked category
        self.display_label = tk.Label(button_frame, text="Bluetooth", bg="white")
        self.display_label.grid(row=2, columnspan=3, sticky="nsew", pady=2)

        # Configure grid weights for responsive resizing
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(1, weight=1)  # Separator
        button_frame.grid_rowconfigure(2, weight=1)  # Label

    def update_status(self, status):
        self.status = status
        self.update_label(f"Selected: {status}")

    def update_label(self, text):
        self.display_label.config(text=text)