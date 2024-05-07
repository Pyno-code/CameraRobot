import asyncio
from bleak import BleakClient
from bleak.exc import BleakError

# Adresse MAC du périphérique BLE auquel se connecter
DEVICE_MAC_ADDRESS = '80:65:99:c8:b4:a1'

# UUID de la caractéristique que nous voulons lire/écrire
CHARACTERISTIC_UUID = "1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e"



async def connect_and_run(address):
    async with BleakClient(address) as client:

        print(f"Connected: {client}")
        while True:
            try:
                # Read value from the characteristic
                # Write value to the characteristic
                # Replace 'your_data' with the data you want to write
                t = input("data : ")
                if t != "quit":
                    data_to_write = bytearray(t.encode())
                    await client.write_gatt_char(CHARACTERISTIC_UUID, data_to_write, response=True)
                    print("Value written:", data_to_write.decode())
                    value = await client.read_gatt_char(CHARACTERISTIC_UUID)
                    print("Value read:", value.decode())
                else:
                    await client.disconnect()
                    break
            except OSError as e:
                print("le client est inacessible 1")
                print(e)
            """except BleakError as e:
                print("le client est inacessible 2")
                print(e)"""


        
            
            
        

async def main():
    await connect_and_run('80:65:99:c8:b4:a1')
try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
