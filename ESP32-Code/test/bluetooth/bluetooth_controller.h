#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <HardwareSerial.h>
#include "bluetooth/characteristic.h"
#include "bluetooth/server.h"

class BluetoothController {
    private:
        ServerBluetooth *pServerBluetooth;
        Characteristic *characteristic1;

    public:
        BluetoothController(std::string deviceName) {
            Serial.println("Initializing Bluetooth Controller");
            BLEDevice::init(deviceName);

            #define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"

            // definier tout les UUID ici
            // https://www.uuidgenerator.net/
            #define CHARACTERISTIC_UUID "1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e"
            // fin des définitions des UUID

            pServerBluetooth = new ServerBluetooth(deviceName, SERVICE_UUID);
            
            // definier toutes les caractéristiques ici
            characteristic1 = new Characteristic(pServerBluetooth->getServer(), SERVICE_UUID, CHARACTERISTIC_UUID);

            pServerBluetooth->startServer();
        }

        void startAdvertising() {
            pServerBluetooth->startAdvertising();
        }

        bool isDeviceConnected() {
            return pServerBluetooth->isDeviceConnected();
        }
        void loop() {
            bool deviceConnected = pServerBluetooth->isDeviceConnected();
            if (!deviceConnected) {
                pServerBluetooth->startAdvertising();
                Serial.println("start advertising");
                delay(2000);

            }
            else {
                Serial.println("device connected");
                // faire des choses ici lors de la connexion
                if (characteristic1->getCallback()->hasValue()) {
                    char* retrievedValue = characteristic1->getCallback()->popValue();
                    Serial.println(retrievedValue);
                }
            }
        }
};
