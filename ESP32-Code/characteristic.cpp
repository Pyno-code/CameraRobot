
#include <iostream>
#include <string>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <HardwareSerial.h>
#include <typeinfo>

class CharacteristicCallBack: public BLECharacteristicCallbacks {
    public:
        std::string value;
        std::string getValue();
        void onWrite(BLECharacteristic *pChar) override {
            value = pChar->getValue();
        }
};

std::string CharacteristicCallBack::getValue(){
    return value;
};

class Characteristic {

    private:

        std::string uuid;
        bool notify;
        bool write;
        bool read;
        BLECharacteristic* pCharacteristic;
        BLE2902 *pBLE2902;
        BLEService *pService;
        CharacteristicCallBack *callback;
        std::string getValue();

    public:
        Characteristic(BLEService *pService_, const std::string& uuid_, const bool notify_ = true, const bool write_ = true, const bool read_ = true)
        : pService(pService_), uuid(uuid_), notify(notify_), write(write_), read(read_) {
            
            pCharacteristic = pService->createCharacteristic(
                uuid,
                BLECharacteristic::PROPERTY_READ   |
                BLECharacteristic::PROPERTY_WRITE  |                      
                BLECharacteristic::PROPERTY_NOTIFY
            );  

            callback = new CharacteristicCallBack();
            pBLE2902 = new BLE2902();
            pBLE2902->setNotifications(true);
            pCharacteristic->addDescriptor(pBLE2902);
            pCharacteristic->setCallbacks(callback);
        }
};

std::string Characteristic::getValue(){
    return callback->getValue();
};

