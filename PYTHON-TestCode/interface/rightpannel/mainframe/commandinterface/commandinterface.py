from multiprocessing import Queue
import queue
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText



class CommandInterface(tk.Frame):

    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    SUCCESS = "SUCCESS"

    def __init__(self, parent, queue_recv_tcp_message: Queue, queue_send_command: Queue, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.queue_recv_tcp_message = queue_recv_tcp_message
        self.queue_send_command = queue_send_command

        # Créer le widget de texte défilant pour afficher les résultats
        self.text_area = ScrolledText(self, wrap=tk.WORD)
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Créer le widget d'entrée de texte
        self.entry = ttk.Entry(self)
        self.entry.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.entry.bind("<Return>", self.execute_command)
        self.entry.bind("<KeyPress-Up>", self.up_command)
        self.entry.bind("<KeyPress-Down>", self.down_command)

        # Désactiver l'édition dans le widget de texte défilant
        self.text_area.configure(state="disabled")
        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.configure_log_tags()

        self.list_command = [""]
        self.command_selector = 0

    def configure_log_tags(self):
        self.text_area.tag_configure(self.FATAL, foreground="red")
        self.text_area.tag_configure(self.ERROR, foreground="red")
        self.text_area.tag_configure(self.WARNING, foreground="orange")
        self.text_area.tag_configure(self.INFO, foreground="blue")
        self.text_area.tag_configure(self.DEBUG, foreground="gray")
        self.text_area.tag_configure(self.SUCCESS, foreground="green")

    def execute_command(self, event):
        # Récupérer la commande saisie par l'utilisateur
        command = self.entry.get()
        # Effacer le contenu de l'entrée de texte
        if command != "":
            if command == "cls":
                self.list_command = [""]
                self.text_area.configure(state="normal")
                self.text_area.delete(1.0, tk.END)
                self.text_area.configure(state="disabled")
            else:
                self.list_command.append(command)
                self.entry.delete(0, tk.END)
                # Envoyer la commande à la file d'attente pour être traitée par le contrôleur
                self.queue_send_command.put(command)
                self.command_selector = len(self.list_command)

    def log(self, queue_logger : queue.Queue):
        self.queue_logger = queue_logger
        for i in range(queue_logger.qsize()):
            if not queue_logger.empty():
                level, message = queue_logger.get()
                self.text_area.configure(state="normal")
                self.text_area.insert(tk.END, f"[{level}] -- {message}\n", level)
                self.text_area.see(tk.END)
                self.text_area.configure(state="disabled")
    
    def up_command(self, event):
        self.command_selector -= 1
        self.update_entry()
    
    def down_command(self, event):
        self.command_selector += 1
        self.update_entry()

    
    def update_entry(self):
        if len(self.list_command) > 0:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.list_command[self.command_selector % len(self.list_command)])


# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1280x720")

    command_interface = CommandInterface(root)
    command_interface.pack(expand=True, fill="both")

    command_interface.log(CommandInterface.INFO, "This is an information message.")
    command_interface.log(CommandInterface.WARNING, "This is a warning message.")
    command_interface.log(CommandInterface.ERROR, "This is an error message.")
    command_interface.log(CommandInterface.FATAL, "This is a fatal message.")
    command_interface.log(CommandInterface.DEBUG, "This is a debug message.")

    root.mainloop()
