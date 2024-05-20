import asyncio
from bleak import BleakClient

class BLEClient:
    def __init__(self, device_address):
        self.device_address = device_address
        self.client = None

    async def connect(self):
        self.client = BleakClient(self.device_address)
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def read_characteristic(self, characteristic_uuid):
        value = await self.client.read_gatt_char(characteristic_uuid)
        return value

    async def write_characteristic(self, characteristic_uuid, data):
        await self.client.write_gatt_char(characteristic_uuid, data)

# Example usage
async def main():
    device_address = "00:11:22:33:AA:BB"  # Replace with your device address
    client = BLEClient(device_address)
    await client.connect()

asyncio.run(main())