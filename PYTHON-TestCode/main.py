import asyncio
import os
from bluetooth_connection.bluetooth_controller import BluetoothController
from interface.interface import App
from os.path import abspath, dirname


if __name__ == "__main__":
    os.chdir(dirname(abspath(__file__)))
    
    
