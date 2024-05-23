
from tkinter import ttk


class LeftFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually
        self.pack_propagate(False)   # Prevent frame from resizing to fit its content

        # Create the Selector widget
        selector = Selector(self)
        selector.grid(row=0, columnspan=1, sticky="nsew")

        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.grid(row=1, columnspan=1, sticky="ew", pady=1)

        # Create the StatusPannel widget
        status_pannel = StatusPannel(self)
        status_pannel.grid(row=2, columnspan=1, sticky="nsew")

        separator2 = ttk.Separator(self, orient='horizontal')
        separator2.grid(row=3, columnspan=1, sticky="ew", pady=1)


        # Create the CommandPannel widget
        command_pannel = CommandPannel(self)
        command_pannel.grid(row=4, columnspan=1, sticky="nsew")

        # Configure grid weights for responsive resizing
        self.grid_rowconfigure(0, weight=1)  # Selector
        self.grid_rowconfigure(1, weight=0)  # Separator
        self.grid_rowconfigure(2, weight=5)  # StatusPannel
        self.grid_rowconfigure(3, weight=0)  # Separator
        self.grid_rowconfigure(4, weight=6)  # CommandPannel
        self.grid_columnconfigure(0, weight=1)