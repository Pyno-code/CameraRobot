
import asyncio
from bluetooth_connection.client import BLEClient
from bluetooth_connection.constants import *
import data.variable

class BluetoothController:
    def __init__(self) -> None:
        self.client = BLEClient()

    async def connect(self):
        return await self.client.connect_by_name("ESP32")
        
    async def loop(self):
        if not self.client.is_connected():
            print("not connected")
            data.variable.logger.log(data.variable.INFO, "trying to connect ...")
            await self.connect()
            await asyncio.sleep(1)
        else:
            await self.update_ble_values()
            await self.read_ble_values()

    async def read_ble_values(self):
        data.variable.bleValues[IP_UUID] = await self.client.read_characteristic(IP_UUID)
        data.variable.bleValues[PORT_UUID] = await self.client.read_characteristic(PORT_UUID)
        data.variable.bleValues[WIFI_STATUS_UUID] = await self.client.read_characteristic(WIFI_STATUS_UUID)
        data.variable.bleValues[WORKING_STATUS_UUID] = await self.client.read_characteristic(WORKING_STATUS_UUID)
        data.variable.bleValues[SERVER_TCP_STATUS_UUID] = await self.client.read_characteristic(SERVER_TCP_STATUS_UUID)

    async def update_ble_values(self):
        await self.update_ble_value(SSID_UUID)
        await self.update_ble_value(PASSWORD_UUID)
        
        await self.update_ble_value(ORDER_WIFI_CONNECTION_UUID)
        await self.update_ble_value(ORDER_WORKING_UUID)

    async def update_ble_value(self, uuid):
        if data.variable.bleValues[uuid] != await self.client.read_characteristic(uuid):
            await self.client.write_characteristic(uuid, data.variable.bleValues[uuid])


# Example usage
async def main():
    device_address = "48:27:E2:63:9E:A5"  # Replace with your device address

    client = BLEClient()
    # await client.scan(debug=True)
    print("Connecting to device...")
    await client.connect_by_name("ESP32")
    print("Connected to device.")

    input("orderworking: true, click enter to continue ...")
    await client.write_characteristic(ORDER_WORKING_UUID, "true")
    print("done")
    

    input("ssid: test, click enter to continue ...")
    await client.write_characteristic(SSID_UUID, "test")
    print("done")


    input("password: 12345678, click enter to continue ...")
    await client.write_characteristic(PASSWORD_UUID, "12345678")
    print("done")

    
    input("orderwifi: true, click enter to continue ...")
    await client.write_characteristic(ORDER_WIFI_CONNECTION_UUID, "true")
    print("done")

    
    time.sleep(1)
    ip = await client.read_characteristic(IP_UUID)
    print("IP :", ip)

    input("orderwifi: false, click enter to continue ...")
    await client.write_characteristic(ORDER_WIFI_CONNECTION_UUID, "false")
    print("done")

    input("orderworking: false, click enter to continue ...")
    await client.write_characteristic(ORDER_WORKING_UUID, "false")
    print("done")
    
    input("disconnect, click enter to continue ...")
    await client.disconnect()
    print("done")
