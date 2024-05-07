#include "bluetooth/bluetooth_controller.h"
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <HardwareSerial.h>

// Initialize all pointers
ServerBluetooth *pServerBluetooth;
Characteristic *characteristic1;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/
// UUIDs used in this example:
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e"


void setup() {
  std::string deviceName = "ESP32";
  Serial.begin(115200);

  BLEDevice::init(deviceName);
  
  pServerBluetooth = new ServerBluetooth(deviceName, SERVICE_UUID);
  characteristic1 = new Characteristic(pServerBluetooth->getServer(), SERVICE_UUID, CHARACTERISTIC_UUID);
  pServerBluetooth->startServer();

}

void loop() {
    // The code below keeps the connection status uptodate:
    // Disconnecting
  bool deviceConnected = pServerBluetooth->isDeviceConnected();
  if (!deviceConnected) {
      delay(2000); // give the bluetooth stack the chance to get things ready
      pServerBluetooth->startAdvertising(); // restart advertising
      Serial.println("start advertising");
  }
  if (deviceConnected) {
    // do stuff here on connecting
    if (characteristic1->getCallback()->hasValue()) {
      char* retrievedValue = characteristic1->getCallback()->popValue();
      Serial.println(retrievedValue);
    }
  }
}
