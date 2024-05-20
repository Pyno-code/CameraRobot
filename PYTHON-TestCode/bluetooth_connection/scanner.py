import asyncio
from bleak import BleakScanner
from bleak.exc import BleakError
from tabulate import tabulate

async def scan():
    try:
        print("Scanning for BLE devices...")

        devices = await BleakScanner.discover()

        if not devices:
            print("No BLE devices found.")
            return

        # Printing zone
        # -----------------------
        data = []
        for index, device in enumerate(devices):
            if device.name is not None:
                data.append([index, device.name, device.address])
        
        headers = ["Index", "Name", "MAC Address"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
        # -----------------------

    except BleakError as e:
        print(f"BleakError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(scan())
