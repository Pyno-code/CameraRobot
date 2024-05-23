import tkinter as tk

class RightFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="white")  # Just to differentiate visually
        self.pack_propagate(False)   # Prevent frame from resizing to fit its content

        # Add content to the right frame (for demonstration purposes)
        right_label = tk.Label(self, text="Right Frame", bg="white")
        right_label.pack(expand=True)