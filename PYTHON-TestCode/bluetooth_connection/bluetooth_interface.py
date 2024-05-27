import asyncio
import tkinter as tk
from tkinter import scrolledtext
from bleak import BleakScanner, BleakError
from client import BLEClient
from constants import *

class AppBluetooth:
    def __init__(self, root):
        self.root = root
        self.client = BLEClient()
        self.setup_gui()
        self.loop = None
        self.running = True
        root.protocol("WM_DELETE_WINDOW", self.on_closing)


    async def run(self):
        self.loop = asyncio.get_event_loop()
        await self.root_loop()


    def on_closing(self):
        self.running = False
        self.root.destroy()

    def setup_gui(self):
        self.root.title("BLE Client")
        
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.text_area.grid(column=0, row=0, padx=10, pady=10, columnspan=2)
        
        self.ssid_label = tk.Label(self.root, text="SSID:")
        self.ssid_label.grid(column=0, row=1, sticky=tk.E)
        self.ssid_entry = tk.Entry(self.root, width=30)
        self.ssid_entry.grid(column=1, row=1)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(column=0, row=2, sticky=tk.E)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.grid(column=1, row=2)

        self.connect_button = tk.Button(self.root, text="Connect", command=lambda: asyncio.create_task(self.connect_device()))
        self.connect_button.grid(column=0, row=3, padx=5, pady=5)

        self.orderworking_button = tk.Button(self.root, text="Set Order Working", command=lambda: asyncio.create_task(self.write_characteristic(ORDER_WORKING_UUID, "true")))
        self.orderworking_button.grid(column=1, row=3, padx=5, pady=5)

        self.set_ssid_button = tk.Button(self.root, text="Set SSID", command=lambda: asyncio.create_task(self.write_characteristic(SSID_UUID, self.ssid_entry.get())))
        self.set_ssid_button.grid(column=0, row=4, padx=5, pady=5)

        self.set_password_button = tk.Button(self.root, text="Set Password", command=lambda: asyncio.create_task(self.write_characteristic(PASSWORD_UUID, self.password_entry.get())))
        self.set_password_button.grid(column=1, row=4, padx=5, pady=5)

        self.orderwifi_button = tk.Button(self.root, text="Order WiFi Connection", command=lambda: asyncio.create_task(self.write_characteristic(ORDER_WIFI_CONNECTION_UUID, "true")))
        self.orderwifi_button.grid(column=0, row=5, padx=5, pady=5)

        self.read_ip_button = tk.Button(self.root, text="Read IP", command=lambda: asyncio.create_task(self.read_ip()))
        self.read_ip_button.grid(column=1, row=5, padx=5, pady=5)

        self.orderwifi_off_button = tk.Button(self.root, text="Order WiFi Disconnect", command=lambda: asyncio.create_task(self.write_characteristic(ORDER_WIFI_CONNECTION_UUID, "false")))
        self.orderwifi_off_button.grid(column=0, row=6, padx=5, pady=5)

        self.orderworking_off_button = tk.Button(self.root, text="Set Order Working Off", command=lambda: asyncio.create_task(self.write_characteristic(ORDER_WORKING_UUID, "false")))
        self.orderworking_off_button.grid(column=1, row=6, padx=5, pady=5)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", command=lambda: asyncio.create_task(self.disconnect_device()))
        self.disconnect_button.grid(column=0, row=7, padx=5, pady=5)

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.yview(tk.END)

    async def connect_device(self):
        self.log("Connecting to device...")
        connected = await self.client.connect_by_name("ESP32")
        if connected:
            self.log("Connected to device.")
        else:
            self.log("Device not found.")

    async def write_characteristic(self, uuid, value):
        await self.client.write_characteristic(uuid, value)
        self.log(f"Wrote {value} to characteristic {UUIDS[uuid]}.")

    async def read_ip(self):
        ip = await self.client.read_characteristic(IP_UUID)
        self.log(f"IP: {ip}")

    async def disconnect_device(self):
        await self.client.disconnect()
        self.log("Disconnected from device.")

    async def root_loop(self):
        while self.running:
            await asyncio.sleep(0.06)  # Allow other tasks to run
            self.root.update()  # Update the tkinter GUI


if __name__ == "__main__":
    root = tk.Tk()
    app = AppBluetooth(root)
    asyncio.run(app.run())
