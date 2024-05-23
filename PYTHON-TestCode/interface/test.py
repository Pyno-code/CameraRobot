import tkinter as tk
from tkinter import ttk

class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.status = "Bluetooth"

        self.config(bg="white")  # Just to differentiate visually
        self.pack_propagate(False)   # Prevent frame from resizing to fit its content

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

class RightFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="white")  # Just to differentiate visually
        self.pack_propagate(False)   # Prevent frame from resizing to fit its content

        # Add content to the right frame (for demonstration purposes)
        right_label = tk.Label(self, text="Right Frame", bg="white")
        right_label.pack(expand=True)

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Responsive Tkinter Window")
        self.geometry("800x600")  # Set initial size of the window

        # Configure the grid to allow responsive resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Create frames
        self.left_frame = LeftFrame(self)
        self.right_frame = RightFrame(self)

        # Create a separator
        self.separator = ttk.Separator(self, orient='vertical')

        # Place frames and separator in the grid
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.separator.grid(row=0, column=1, sticky="ns")
        self.right_frame.grid(row=0, column=2, sticky="nsew")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
