import tkinter as tk

def foo():
    pass

class ToggleSwitch(tk.Button):
    def __init__(self, parent, func=foo, **kwargs):
        super().__init__(parent, **kwargs)
        self.func = func
        self.state = False
        self.configure(bg='red', activebackground='red', relief='sunken')
        self.bind('<Button-1>', self.toggle)

    def toggle(self, event):
        self.state = not self.state

        if self.state:
            self.configure(bg='green', activebackground='green', relief='raised')
        else:
            self.configure(bg='red', activebackground='red', relief='sunken')
        
        self.func()
    
    def get_state(self):
        return self.state
            



# Example usage
if __name__ == '__main__':
    root = tk.Tk()
    toggle_switch = ToggleSwitch(root, width=100, height=50)
    toggle_switch.pack()
    root.mainloop()