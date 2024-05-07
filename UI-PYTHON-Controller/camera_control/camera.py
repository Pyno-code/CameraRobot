import time
import pygame
import cv2
from camera_control.popup_controller import GestionCamera, PopUpError
from timer_module.time_calcul import TimerThread
import tutorial_modules.tutorial_5_connect_wifi.wifi_enable as wifi_enable
import asyncio
import camera_control.controller_wifi as controller_wifi
from multi_webcam.webcam import Webcam

class Camera(pygame.sprite.Sprite):

    def __init__(self, window: pygame.Surface) -> None:
        super().__init__()
        
        self.current_frame = pygame.surface.Surface((0, 0))
        self.camera_alive = False

        self.init = False
        self.pop_up_controller = GestionCamera()
        self.pop_up_controller.activer_camera()

        mode = self.pop_up_controller.mode

        self.pop_up_window = PopUpError()
        self.window = window
        print(mode)

        if mode == self.pop_up_controller.list_mode[self.pop_up_controller.GOPRO]:
            asyncio.run(self.init_camera_from_gopro())
        elif mode == self.pop_up_controller.list_mode[self.pop_up_controller.IP]:
            self.init_camera_from_ip()
        else:
            self.camera_alive = False
            self.init = True

        self.mode = mode
        
        while not self.init:
            time.sleep(0.5)

    async def init_camera_from_gopro(self):
        enable_wifi = asyncio.create_task(wifi_enable.enable_wifi(None))
        ssid, password, client = await enable_wifi
        print("-------------------------")
        while not (ssid in controller_wifi.displayAvailableNetworks()):
            time.sleep(0.2)
        controller_wifi.createNewConnection(ssid, ssid, password)
        controller_wifi.connect(ssid, ssid)
        print("-------------------------")


        readytogo = False
        while not readytogo:
            try:
                webcam = Webcam(serial="174")  # 11
                webcam.start(9000)
                readytogo = True
            except Exception as e:
                time.sleep(0.5)
                print(e)

    

        print("camera enable")
        port = 9000
        url = f"udp://0.0.0.0:{port}"
        #webcam.start(port=port)

        print("camera streaming at :", url)

        print("-------------------------")

        # Capture video from webcam
        cap = cv2.VideoCapture(url + "?overrun_nonfatal=1&fifo_size=50000000", cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.init = True


    def init_camera_from_ip(self):
        self.stream = cv2.VideoCapture(f'http://{self.pop_up_controller.get_ip()}:8080/video')
        fps = self.stream.get(cv2.CAP_PROP_FPS)

        print("fps :", fps)

        width  = self.stream.get(3)   # float `width`
        height = self.stream.get(4)  # float `height`

        self.counter = 0

        print("camera alive", self.camera_alive)
        self.frame = TimerThread(self.frame, 0)
        self.get_frame()

        self.init = True

    def get_frame(self):
        try:
            self.frame()
            self.camera_alive = True
        except:
            self.camera_alive = False
            self.current_frame = pygame.surface.Surface((0, 0))
            print("Error : cannot get the next frame \nCamera disable from now")
        return self.current_frame

    def frame(self) -> pygame.Surface:
        start = time.time()
        if self.camera_alive:
            ret, frame = self.stream.read()
            #print("start camera get frame", start - time.time())

            self.counter += 1

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 0)
            frame = cv2.rotate(frame, 0)
            self.current_frame = pygame.surfarray.make_surface(frame)

        # print("camera", start - time.time())


         
