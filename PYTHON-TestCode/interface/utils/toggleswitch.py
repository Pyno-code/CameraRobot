import tkinter as tk

class ToggleSwitch(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.state = False
        self.configure(bg='red', activebackground='red', relief='sunken')
        self.bind('<Button-1>', self.toggle)

    def toggle(self, event):
        if self.state:
            self.configure(bg='red', activebackground='red', relief='sunken')
        else:
            self.configure(bg='green', activebackground='green', relief='raised')
        self.state = not self.state

# Example usage
if __name__ == '__main__':
    root = tk.Tk()
    toggle_switch = ToggleSwitch(root, width=100, height=50)
    toggle_switch.pack()
    root.mainloop()