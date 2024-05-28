import asyncio
import multiprocessing

from multiprocessing import Process, Manager
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.interface import App
from bluetooth_connection.constants import *




class ManagerController:

    def __init__(self) -> None:
        self.manager = Manager()

        self.running = self.manager.Value('b', True)

        self.queue_logger = self.manager.Queue()

        self.bluetooth_dict_values = self.manager.dict()

        # --------------------------------
        self.bluetooth_dict_values[IP_UUID] = "None"
        self.bluetooth_dict_values[PORT_UUID] = "None"
        
        self.bluetooth_dict_values[SSID_UUID] = "None"
        self.bluetooth_dict_values[PASSWORD_UUID] = "None"
        
        self.bluetooth_dict_values[WIFI_STATUS_UUID] = "false"
        self.bluetooth_dict_values[WORKING_STATUS_UUID] = "false"
        self.bluetooth_dict_values[SERVER_TCP_STATUS_UUID] = "false"
        
        self.bluetooth_dict_values[ORDER_WIFI_CONNECTION_UUID] = "false"
        self.bluetooth_dict_values[ORDER_WORKING_UUID] = "false"
        # --------------------------------

        

        self.bluetooth_order_dict = self.manager.dict()

        self.bluetooth_order_dict["BLUETOOTH_CONNECTION"] = "false"
        self.bluetooth_order_dict["BLUETOOTH_UPDATE"] = "false"
        self.bluetooth_order_dict["WIFI_CONNECTION"] = "false"
        self.bluetooth_order_dict["WIFI_UPDATE"] = "false"

        self.wifi_order_event = self.manager.Queue()
        self.wifi_update_event = self.manager.Queue()

        self.bluetooth_controller = BluetoothController(self.running, self.bluetooth_dict_values, self.bluetooth_order_dict, self.queue_logger)
        self.interface_controller = App(self.running, self.wifi_update_event, self.wifi_order_event, self.bluetooth_dict_values, self.bluetooth_order_dict, self.queue_logger)
        
        self.bluetooth_process = Process(target=self.bluetooth_controller.start)


    def stop(self):
        self.running.value = False

    def launch(self):
        self.bluetooth_process.start()
        self.interface_controller.start()

    def join(self):
        self.bluetooth_process.join()
        
        