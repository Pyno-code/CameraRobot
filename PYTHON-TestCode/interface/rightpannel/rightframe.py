import tkinter as tk
from interface.rightpannel.toolbar.toolbar import Toolbar
from interface.rightpannel.mainframe.mainframe import MainFrame

class RightFrame(tk.Frame):
    def __init__(self, parent, queue_recv_tcp_message, queue_send_tcp_message, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="white")  # Just to differentiate visually

        # Créer la toolbar
        self.toolbar = Toolbar(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Créer le mainframe
        self.main_frame = MainFrame(self, queue_recv_tcp_message, queue_send_tcp_message)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Lier les boutons de la toolbar aux méthodes de changement de vue
        self.toolbar.bind_camera(self.main_frame.show_camera)
        self.toolbar.bind_command_interface(self.main_frame.show_command_interface)

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")

    right_frame = RightFrame(root)
    right_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
