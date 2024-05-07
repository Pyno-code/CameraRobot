#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <HardwareSerial.h>
#include "bluetooth/characteristic.h"
#include "bluetooth/server.h"


#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"


class BluetoothController {
    private:
        ServerBluetooth *pServerBluetooth;
        bool isRunning = false;
        std::map<std::string, Characteristic*>* characteristics;


        ~BluetoothController() {
                    if (isRunning) {
                        stop();
                    }
                }
    public:
        BluetoothController(std::string deviceName) {
            Serial.println("Initializing Bluetooth Controller");
            BLEDevice::init(deviceName);


            // definier tout les UUID ici
            // https://www.uuidgenerator.net/
            #define CHARACTERISTIC_UUID "1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e"
            #define SSID_UUID "02456daf-2ff7-431b-812b-772f0eb7b2b2"
            #define PASSWORD "ebac488a-1cd1-4bdf-b6a6-9fc78fe75772"


            // fin des définitions des UUID

            pServerBluetooth = new ServerBluetooth(deviceName, SERVICE_UUID);
            //cré les caractéristiques et ensuite start le serveur
            Characteristic ssid = *createCharacteristic(SSID_UUID);
            Characteristic password = *createCharacteristic(PASSWORD);
            
        }

        Characteristic* createCharacteristic(const char* uuid) {
            Characteristic *characteristic = new Characteristic(pServerBluetooth->getServer(), SERVICE_UUID, uuid);
            (*characteristics)[uuid] = characteristic;
            return characteristic;
        }

        void startServer() {
            pServerBluetooth->startServer();
            isRunning = true;
        }

        void startAdvertising() {
            pServerBluetooth->startAdvertising();
        }

        bool isDeviceConnected() {
            return pServerBluetooth->isDeviceConnected();
        }

        // Cette fonction est un exemple de l'utilisation du contrôleur, elle ne doit pas être appelée.
        void loop() {
            bool deviceConnected = pServerBluetooth->isDeviceConnected();
            if (!deviceConnected) {
                pServerBluetooth->startAdvertising();
                delay(2000);
            }
            else {
                // faire des choses ici lors de la connexion
                
                //recuperer la premiere charactéristique et afficher sa valeur
                
                // modulo qu'il y est une characteristique
                if (!characteristics->empty()) {
                    std::map<std::string, Characteristic*>::iterator it = characteristics->begin();
                    std::string uuid = it->first;
                    Characteristic* characteristic1 = it->second;

                    // et qu'il y est une valeur à afficher
                    if (characteristic1->getCallback()->hasValue()) {
                        char* retrievedValue = characteristic1->getCallback()->popValue();
                        Serial.println(retrievedValue);
                    }
                }
                
            }
        }

        void stop() {
            pServerBluetooth->stopServer();
            characteristics->clear();
            delete characteristics;
            delete pServerBluetooth;
            isRunning = false;
        }

        bool hasStoped() {
            return !isRunning;
        }

        Characteristic* getCharacteristic(const char* uuid) {
            return (*characteristics)[uuid];
        }
};
