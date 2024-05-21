import asyncio
import time
from bleak import BleakClient

from client import BLEClient
from constants import *


client = BLEClient()
async def connect_to_server(address):
    client = BleakClient(address)
    await client.connect()
    time.sleep(3)

    data = await client.read_gatt_char(ORDER_WORKING_UUID)
    print(data.decode("utf-8"))

    time.sleep(3)

    await client.write_gatt_char(ORDER_WORKING_UUID, bytearray("false", "utf-8"))

    time.sleep(3)

    # Faire quelque chose avec le client connecté
    # Par exemple, lire des caractéristiques ou écrire des données

    # Déconnexion du serveur BLE
    await client.disconnect()




# Adresse MAC du serveur BLE
device_address = "48:27:E2:63:9E:A5"  

# Lancement de la connexion au serveur BLE
# asyncio.run(client.scan(debug=True))
asyncio.run(connect_to_server(device_address))