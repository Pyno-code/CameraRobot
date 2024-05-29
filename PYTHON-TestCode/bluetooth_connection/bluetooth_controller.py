
import asyncio
from bluetooth_connection.client import BLEClient
from bluetooth_connection.constants import *
from multiprocessing import Value, Queue
import traceback

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
            try:

                if self.order_dict["BLUETOOTH_CONNECTION"] == "true":
                    if not self.client.is_connected():
                        self.queue_logger.put(('INFO', "Trying to connect ..."))
                        connected = await self.connect()

                        self.shared_dict["BLUETOOTH_CONNECTED"] = "true" if connected else "false"

                        if connected:
                            self.queue_logger.put(('SUCCESS', "Connected to the bluetooth"))
                        else:
                            self.queue_logger.put(('WARNING', "Failed to connect to the bluetooth"))
                            await asyncio.sleep(1)
                    else:
                        if self.order_dict["BLUETOOTH_UPDATE"] == "true":
                            # self.queue_logger.put(('DEBUG', f"Working value : {self.shared_dict[WORKING_STATUS_UUID]}"))
                            current_shared_dict = self.shared_dict.copy()

                            # faire avant l'écriture des valeurs 
                            read_uuids_updated = await self.read_ble_values()
                            if WIFI_STATUS_UUID in read_uuids_updated:
                                if self.shared_dict[WIFI_STATUS_UUID] == "true":
                                    self.queue_logger.put(('SUCCESS', "Connected to the wifi"))
                                elif self.shared_dict[WIFI_STATUS_UUID] == "false":
                                    self.queue_logger.put(('WARNING', "Disconnected from the wifi"))
                            
                            # à faire apres la lecture des valeurs, tres important !
                            await self.update_ble_values(current_shared_dict)
                            await asyncio.sleep(1)
                            
                else:
                    if self.client.is_connected():
                        await self.client.disconnect()
                        self.queue_logger.put(('WARNING', "Disconnected from the bluetooth"))

                    self.shared_dict[IP_UUID] = ""
                    self.shared_dict[PORT_UUID] = ""
                    self.shared_dict[ADDRESS_MAC_UUID] = ""
                    self.shared_dict[WIFI_STATUS_UUID] = "false"
                    self.shared_dict[WORKING_STATUS_UUID] = "false"
                    self.shared_dict[SERVER_TCP_STATUS_UUID] = "false"
                    
                    self.shared_dict[SSID_UUID] = ""
                    self.shared_dict[PASSWORD_UUID] = ""
                    self.shared_dict[ORDER_WIFI_CONNECTION_UUID] = "false"
                    self.shared_dict[ORDER_WORKING_UUID] = "false"
                    self.shared_dict[ORDER_TCP_CONNECTION_UUID] = "false"

                    self.shared_dict["BLUETOOTH_CONNECTED"] = "false"


                    await asyncio.sleep(3)
            except Exception as e:
                traceback_str = traceback.format_exc()
                self.queue_logger.put(('ERROR',  traceback_str))
                print(traceback_str)



    async def read_ble_values(self):
        
        updated_values = []

        for uuid in UUIDS_INFO:
            if await self.client.read_characteristic(uuid) != self.shared_dict[uuid]:
                updated_values.append(uuid)
                self.shared_dict[uuid] = await self.client.read_characteristic(uuid)

        return updated_values
        # check if different from the the dict queue value

    async def update_ble_values(self, current_shared_dict):
        for uuid in UUIDS_SEND_INFO + UUIDS_ORDER:
            if current_shared_dict[uuid] != await self.client.read_characteristic(uuid):
                await self.client.write_characteristic(uuid, current_shared_dict[uuid])
        
  
    def start(self):
        asyncio.run(self.loop())

