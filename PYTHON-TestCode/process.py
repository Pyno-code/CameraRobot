import asyncio
import multiprocessing

from multiprocessing import Process, Manager
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.interface import App
from tcp_connection.tcp_controller import TCPController
from bluetooth_connection.constants import *




class ManagerController:

    def __init__(self) -> None:
        self.manager = Manager()

        self.running = self.manager.Value('b', True)

        self.queue_logger = self.manager.Queue()

        self.dict_values = self.manager.dict()

        # --------------------------------
        self.dict_values[IP_UUID] = "None"
        self.dict_values[PORT_UUID] = "None"
        
        self.dict_values[SSID_UUID] = "None"
        self.dict_values[PASSWORD_UUID] = "None"
        
        self.dict_values[WIFI_STATUS_UUID] = "false"
        self.dict_values[WORKING_STATUS_UUID] = "false"
        self.dict_values[SERVER_TCP_STATUS_UUID] = "false"
        
        self.dict_values[ORDER_WIFI_CONNECTION_UUID] = "false"
        self.dict_values[ORDER_WORKING_UUID] = "false"

        # --------------------------------
        self.dict_values["TCP_CONNECTED"] = "false"
        

        self.order_dict = self.manager.dict()
        
        self.order_dict["BLUETOOTH_CONNECTION"] = "false"
        self.order_dict["BLUETOOTH_UPDATE"] = "false"
        self.order_dict["WIFI_CONNECTION"] = "false"
        self.order_dict["TCP_CONNECTION"] = "false"
        self.order_dict["TCP_UPDATE"] = "false"

        self.queue_logger.put(('INFO', "Manager initialized"))

        self.queue_send_tcp_message = self.manager.Queue()
        self.queue_recv_tcp_message = self.manager.Queue()

        self.bluetooth_controller = BluetoothController(self.running, self.dict_values, self.order_dict, self.queue_logger)
        self.interface_controller = App(self.running, self.dict_values, self.order_dict, self.queue_logger, self.queue_recv_tcp_message, self.queue_send_tcp_message)
        self.tcp_controller = TCPController(self.running, self.queue_logger, self.queue_send_tcp_message, self.queue_recv_tcp_message, self.order_dict, self.dict_values)

        self.bluetooth_process = Process(target=self.bluetooth_controller.start)
        self.tcp_process = Process(target=self.tcp_controller.start)


    def stop(self):
        self.running.value = False

    def launch(self):
        self.bluetooth_process.start()
        self.tcp_process.start()
        self.interface_controller.start()


    def join(self):
        self.bluetooth_process.join()
        self.tcp_process.join()
        self.manager.shutdown()
        self.manager.join()
        
        