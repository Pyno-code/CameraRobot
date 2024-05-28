
import asyncio
from bluetooth_connection.client import BLEClient
from bluetooth_connection.constants import *
import json
from multiprocessing import Value, Queue

class BluetoothController:
    
    

    def __init__(self, running,  shared_dict, order_dict, queue_logger: Queue) -> None:
        self.client = BLEClient()
        self.running = running

        self.shared_dict = shared_dict
        self.order_dict = order_dict
        self.queue_logger = queue_logger



    async def connect(self):
        return await self.client.connect_by_name("ESP32")
        
    async def loop(self):
        while self.running.value:
            if self.order_dict["BLUETOOTH_CONNECTION"] == "true":
                if not self.client.is_connected():
                    self.queue_logger.put(('INFO', "trying to connect ..."))
                    connected = await self.connect()

                    if connected:
                        self.queue_logger.put(('SUCCESS', "connected to the bluetooth"))
                    else:
                        self.queue_logger.put(('WARNING', "failed to connect to the bluetooth"))
                        await asyncio.sleep(1)
                else:
                    if self.order_dict["BLUETOOTH_UPDATE"] == "true":
                        await self.read_ble_values()
                        await self.update_ble_values()
            else:
                if self.client.is_connected():
                    self.client.disconnect()
                    self.queue_logger.put(('INFO', "disconnected from the bluetooth"))

                self.shared_dict[IP_UUID] = ""
                self.shared_dict[PORT_UUID] = ""
                self.shared_dict[WIFI_STATUS_UUID] = "false"
                self.shared_dict[WORKING_STATUS_UUID] = "false"
                self.shared_dict[SERVER_TCP_STATUS_UUID] = "false"
                
                self.shared_dict[SSID_UUID] = ""
                self.shared_dict[PASSWORD_UUID] = ""
                self.shared_dict[ORDER_WIFI_CONNECTION_UUID] = "false"
                self.shared_dict[ORDER_WORKING_UUID] = "false"

                # self.queue_logger.put(('Debug', self.shared_dict))

                await asyncio.sleep(3)


    async def read_ble_values(self):
        self.shared_dict[IP_UUID] = await self.client.read_characteristic(IP_UUID)
        self.shared_dict[PORT_UUID] = await self.client.read_characteristic(PORT_UUID)
        self.shared_dict[WIFI_STATUS_UUID] = await self.client.read_characteristic(WIFI_STATUS_UUID)
        self.shared_dict[WORKING_STATUS_UUID] = await self.client.read_characteristic(WORKING_STATUS_UUID)
        self.shared_dict[SERVER_TCP_STATUS_UUID] = await self.client.read_characteristic(SERVER_TCP_STATUS_UUID)

        # check if different from the the dict queue value

    async def update_ble_values(self):
        # check if different from the the dict queue value to update the ble value
        await self.update_ble_value(SSID_UUID)
        await self.update_ble_value(PASSWORD_UUID)

        await self.update_ble_value(ORDER_WIFI_CONNECTION_UUID)
        await self.update_ble_value(ORDER_WORKING_UUID)

    async def update_ble_value(self, uuid):
        if self.shared_dict != await self.client.read_characteristic(uuid):
            await self.client.write_characteristic(uuid, self.shared_dict[uuid])

    def start(self):
        asyncio.run(self.loop())

