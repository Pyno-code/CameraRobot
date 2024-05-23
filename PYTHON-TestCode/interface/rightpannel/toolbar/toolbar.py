import tkinter as tk

class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Bouton pour la caméra
        self.camera_button = tk.Button(self, text="Caméra")
        self.camera_button.grid(row=0, column=0, padx=2, pady=5, sticky="nsew")

        # Bouton pour l'interface de commande
        self.command_button = tk.Button(self, text="Commande")
        self.command_button.grid(row=0, column=1, padx=2, pady=5, sticky="nsew")
        tk.Frame(self).grid(row=0, column=2, padx=2, pady=5, sticky="nsew")
        # Configure rows and columns
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=6)

    def bind_camera(self, command):
        self.camera_button.config(command=command)
    
    def bind_command_interface(self, command):
        self.command_button.config(command=command)

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x50")

    toolbar = Toolbar(root)
    toolbar.pack(fill="both", expand=True)

    root.mainloop()
