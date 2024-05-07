from tkinter import messagebox
from tkinter.simpledialog import askstring

class GestionCamera:
    IP = 0
    GOPRO = 1
    NONE = 2
    list_mode = ["IP", "GOPRO", "NONE"]

    def __init__(self):
        self.ip_camera = None
        self.response = False

        self.mode = self.list_mode[2]

    def activer_camera(self):
        response_activation = messagebox.askyesno("Activation de la caméra", "Voulez-vous activer la caméra ?")
        if response_activation:
            response = messagebox.askyesno("Activation de la caméra", "Voulez-vous conecter une GoPro")
            self.mode = self.list_mode[int(response)]
        
        if self.mode == self.list_mode[0]:
            self.ip_camera = askstring("Adresse IP", "Veuillez entrer l'adresse IP de la caméra :")
            print("self.ip_camera : " + str(self.ip_camera))
            if str(self.ip_camera) == "":
                self.ip_camera = None
        
            if self.ip_camera is None:
                self.mode = self.list_mode[2]

        if not response_activation:
            self.mode = self.list_mode[2] 

        return self.mode
    
    def get_ip(self):
        return self.ip_camera

class PopUpError:

    def __init__(self) -> None:
        pass

    def show_erreur(self):
        messagebox.showerror("Erreur Camera", "Fail to connect to the camera")
