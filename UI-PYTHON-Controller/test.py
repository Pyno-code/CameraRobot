import time
import tutorial_modules.tutorial_5_connect_wifi.wifi_enable as wifi_enable
import asyncio
import camera_control.controller_wifi as controller_wifi
from multi_webcam.webcam import Webcam
from camera_control.camera import Camera
import cv2

async def main():
    enable_wifi = asyncio.create_task(wifi_enable.enable_wifi(None))
    ssid, password, client = await enable_wifi
    while not (ssid in controller_wifi.displayAvailableNetworks()):
        time.sleep(0.2)
    controller_wifi.createNewConnection(ssid, ssid, password)
    controller_wifi.connect(ssid, ssid)


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


    # Capture video from webcam
    cap = cv2.VideoCapture(url + "?overrun_nonfatal=1&fifo_size=50000000", cv2.CAP_FFMPEG)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Video Stream', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()
    webcam.disable()
    webcam.stop()

asyncio.run(main())
