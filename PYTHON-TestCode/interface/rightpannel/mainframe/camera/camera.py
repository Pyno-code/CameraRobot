import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CameraWidget(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg="white")
        # Capturer le flux vidéo en direct
        self.capture = cv2.VideoCapture(0)

        # Ajouter un gestionnaire d'événements pour détecter le changement de taille de la fenêtre parent
        parent.bind("<Configure>", self.on_parent_resize)
        self.resizing = False

        self.parent = parent

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.show_video = True

        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()


    def turn_off(self):
        self.show_video = False
    
    def turn_on(self):
        self.show_video = True

    def on_parent_resize(self, event):
        # Redimensionner le widget pour conserver le rapport d'aspect 16:9
        if self.resizing:
            return
        self.resizing = True

        self.width = self.parent.winfo_width()
        self.height = self.parent.winfo_height()
        
        if self.width / self.height > 16 / 9:
            self.width = int(self.height / 9 * 16)
        else:
            self.height = int(self.width / 16 * 9)
        
        self.resizing = False

    async def update_video(self):
        if not self.resizing and self.show_video:
            # Lire une image à partir du flux vidéo
            ret, frame = self.capture.read()
            if ret:
                # Redimensionner l'image pour correspondre à la taille du widget
                frame = cv2.resize(frame, (self.width, self.height))

                # Convertir l'image OpenCV en image Tkinter
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image=image)

                # Effacer le canevas avant de dessiner la nouvelle image
                self.delete("all")

                # Calculer les coordonnées pour centrer l'image sur le canevas
                x = (self.parent.winfo_width() - self.width) // 2
                y = (self.parent.winfo_height() - self.height) // 2
                # Dessiner l'image sur le canevas en utilisant les coordonnées centrées
                self.create_image(x, y, anchor=tk.NW, image=image, tags="video")

                # Garder une référence à l'image pour éviter la suppression par le garbage collector
                self.image = image
            # Planifier la prochaine mise à jour après un certain délai (en millisecondes)
            

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x450")  # Taille initiale en 16:9

    # Créer le widget CameraWidget
    camera_widget = CameraWidget(root)
    camera_widget.pack(expand=True, fill="both")

    # Centrer le widget CameraWidget

    root.mainloop()
