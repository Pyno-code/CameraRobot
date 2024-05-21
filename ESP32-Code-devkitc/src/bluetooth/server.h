#include <BLEServer.h>
#include <BLEDevice.h>
#include <HardwareSerial.h>

class ServerCallback: public BLEServerCallbacks {

    public:
        bool isConnected() {
            return deviceConnected;
        };

    private:
        bool deviceConnected = false;

        void onConnect(BLEServer* pServer) {
            deviceConnected = true;
            Serial.println("Device connected");
        };

        void onDisconnect(BLEServer* pServer) {
            Serial.println("Device disconnected");
            deviceConnected = false;
        };
};


class ServerBluetooth {

    private:
        BLEServer *pServer;
        BLEService *pService;
        ServerCallback *pServerCallback;
        BLEAdvertising *pAdvertising;
        bool isAdvertising = false;

    public:
        ServerBluetooth(std::string deviceName, const std::string& SERVICE_UUID) {            
            BLEAddress bleAddress = BLEDevice::getAddress();
            Serial.print("Adresse Mac : " );
            Serial.println(bleAddress.toString().c_str());
            
            pServer = BLEDevice::createServer();
            pServerCallback = new ServerCallback();
            pServer->setCallbacks(pServerCallback);

            pService = pServer->createService(SERVICE_UUID, 32);

            /*BLECharacteristic* pCharacteristic_2 = pService->createCharacteristic(
                      "1c95d5e3-d8f7-413a-bf3d-7a2e5d7be87e",
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |                      
                      BLECharacteristic::PROPERTY_NOTIFY
                    );
            
            BLE2902* pBLE2902_2 = new BLE2902();
            pBLE2902_2->setNotifications(true);
            pCharacteristic_2->addDescriptor(pBLE2902_2);
            pCharacteristic_2->setValue("nothing");*/
        };

        void startAdvertising() {
            //BLEDevice::startAdvertising();
            if (!isDeviceConnected()) {
                isAdvertising = false;
            }
            if (!isAdvertising) {
                pServer->startAdvertising();
                isAdvertising = true;
            }
        };

        void stopAdvertising() {
            if (isAdvertising) {
                Serial.println("stoping ble signal");
                pAdvertising->stop();
                isAdvertising = false;
            }
        };

        bool isDeviceConnected() {
            return pServerCallback->isConnected();
        };

        void startServer() {
            pService->start();
            pAdvertising = BLEDevice::getAdvertising();

            pAdvertising->addServiceUUID(pService->getUUID());
            pAdvertising->setScanResponse(false);
            pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
            startAdvertising();
            Serial.println("Waiting a client connection to notify...");
        };

        BLEServer *getServer() {
            return pServer;
        };
        
        void stopServer() {
            if (pServer != nullptr) {
                delete pServer;
                pServer = nullptr;
            }
        }

        
};