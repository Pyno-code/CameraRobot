
import asyncio
from multiprocessing import Process, Manager
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.interface import App

class Process:

    def __init__(self) -> None:
        self.manager = Manager()

        self.interface = App()
        self.bluetooth_controller_process = Process(target=self.launch_bluetooth)
        self.interface_process = Process(target=self.interface.mainloop)

    def launch_interface(self):
        asyncio.run(self.interface.start())

    def launch_bluetooth(self):
        self.bluetooth_controller = BluetoothController()
        asyncio.run(self.bluetooth_controller.loop())




