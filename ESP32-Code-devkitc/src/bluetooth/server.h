#include <BLEServer.h>
#include <BLEDevice.h>
#include <HardwareSerial.h>
#include "logger.h"

class ServerCallback: public BLEServerCallbacks {

    public:
        bool isConnected() {
            return deviceConnected;
        };

    private:
        bool deviceConnected = false;

        void onConnect(BLEServer* pServer) {
            deviceConnected = true;
            logger::print(logger::INFO, "Device connected ...");
        };

        void onDisconnect(BLEServer* pServer) {
            logger::print(logger::INFO, "Device disconnected ...");
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
        wServerBluetooth(std::string deviceName, const std::string& SERVICE_UUID) {            
            BLEAddress bleAddress = BLEDevice::getAddress();
            logger::print(logger::INFO, "Adresse Mac : ", false);
            Serial.println(bleAddress.toString().c_str());
            
            pServer = BLEDevice::createServer();
            pServerCallback = new ServerCallback();
            pServer->setCallbacks(pServerCallback);

            pService = pServer->createService(SERVICE_UUID, 32);
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
                logger::print(logger::INFO, "stoping ble signal");
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
            logger::print(logger::INFO, "Waiting a client connection to notify...");
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