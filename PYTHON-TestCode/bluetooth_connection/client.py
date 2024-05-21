import asyncio
from bleak import BleakClient
from bleak import BleakScanner
from bleak.exc import BleakError
from tabulate import tabulate

class BLEClient:
    def __init__(self):
        self.device_address = None
        self.client = None

    async def connect_by_address(self, device_address):
        self.client = BleakClient(self.device_address)
        await self.client.connect()
        return self.client.is_connected
    
    async def connect_by_name(self, device_name):
        devices = await self.scan()
        for device in devices:
            if device.name == device_name:
                self.client = BleakClient(device.address)
                await self.client.connect()
                return self.client.is_connected

    async def disconnect(self):
        await self.client.disconnect()

    async def read_characteristic(self, characteristic_uuid):
        value = await self.client.read_gatt_char(characteristic_uuid)
        return value

    async def write_characteristic(self, characteristic_uuid, data):
        await self.client.write_gatt_char(characteristic_uuid, data)


    async def scan(self, debug=False):
        try:
            print("Scanning for BLE devices...")

            devices = await BleakScanner.discover()            

        except BleakError as e:
            print(f"BleakError occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        if not devices:
            print("No BLE devices found.")

        if debug:
            self.show_devices(devices)

        return devices    

    def show_devices(self, devices):
        data = []
        for index, device in enumerate(devices):
            if device.name is not None:
                data.append([index, device.name, device.address])
        
        headers = ["Index", "Name", "MAC Address"]
        print(tabulate(data, headers=headers, tablefmt="grid"))


# Example usage
async def main():
    device_address = "00:11:22:33:AA:BB"  # Replace with your device address

    client = BLEClient(device_address)
    await client.scan(debug=True)
    # await client.connect()

asyncio.run(main())