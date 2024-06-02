import tkinter as tk
from interface.rightpannel.mainframe.camera.camera import CameraWidget
from interface.rightpannel.mainframe.commandinterface.commandinterface import CommandInterface

class MainFrame(tk.Frame):
    def __init__(self, parent, queue_recv_tcp_message, queue_send_command, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Créer le widget de la caméra
        self.camera_widget = CameraWidget(self)

        # Créer l'interface de commande
        self.command_interface = CommandInterface(self, queue_recv_tcp_message, queue_send_command)

        # Afficher la caméra par défaut
        self.show_command_interface()

    def show_camera(self):
        self.command_interface.pack_forget()
        self.camera_widget.pack(fill=tk.BOTH, expand=True)
    
    def show_command_interface(self):
        self.camera_widget.pack_forget()
        self.command_interface.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    main_frame = MainFrame(root, bg="white")

    # Toolbar or buttons to switch views
    toolbar = tk.Frame(root, bg="white")
    toolbar.pack(side=tk.TOP, fill=tk.X)

    btn_show_camera = tk.Button(toolbar, text="Show Camera", command=main_frame.show_camera)
    btn_show_camera.pack(side=tk.LEFT, padx=5, pady=5)

    btn_show_command = tk.Button(toolbar, text="Show Command Interface", command=main_frame.show_command_interface)
    btn_show_command.pack(side=tk.LEFT, padx=5, pady=5)

    main_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()