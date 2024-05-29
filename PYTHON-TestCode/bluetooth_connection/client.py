import asyncio
import time
from bleak import BleakClient
from bleak import BleakScanner
import bleak
from bleak.exc import BleakError
from tabulate import tabulate
from bluetooth_connection.constants import *



class BLEClient:
    def __init__(self):
        self.device_address = None
        self.client = None

    async def connect_by_address(self, device_address):
        self.client = BleakClient(device_address)
        await self.client.connect()
        return self.is_connected()
    
    async def connect_by_name(self, device_name):
        devices = await self.scan()
        for device in devices:
            if device.name == device_name:
                self.client = BleakClient(device.address)
                try:
                    await self.client.connect()
                except bleak.exc.BleakDeviceNotFoundError:
                    pass
                return self.is_connected()

    async def disconnect(self):
        await self.client.disconnect()

    async def read_characteristic(self, characteristic_uuid):
        try:
            value = await self.client.read_gatt_char(characteristic_uuid)
            return value.decode("utf-8")
        except Exception as e:
            self.client.disconnect()
            raise e

    async def write_characteristic(self, characteristic_uuid, data):
        try:
            await self.client.write_gatt_char(characteristic_uuid, bytearray(data, "utf-8"))
        except Exception as e:
            self.client.disconnect()
            raise e


    async def scan(self, debug=False):
        try:
            if debug:
                print("Scanning for BLE devices...")
            devices = []
            devices = await BleakScanner.discover()         

        except BleakError as e:
            print(f"BleakError occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        if not devices:
            print("No BLE devices found.")

        if debug:
            self.show_devices(devices)
        await asyncio.sleep(1)
        return devices    

    def show_devices(self, devices):
        data = []
        for index, device in enumerate(devices):
            if device.name is not None:
                data.append([index, device.name, device.address])
        
        headers = ["Index", "Name", "MAC Address"]
        print(tabulate(data, headers=headers, tablefmt="grid"))


    def is_connected(self):
        if self.client is not None:
            return self.client.is_connected
        return False

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

if __name__ == "__main__":
    asyncio.run(main())