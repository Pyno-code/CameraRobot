#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <stdio.h>
#include <string.h>
#include <queue>

class CharacteristicCallBack : public BLECharacteristicCallbacks {
private:
    std::queue<char*> list_queue;

public:
    char* popValue() {
        if (!list_queue.empty()) {
            char* value_ = list_queue.front();
            list_queue.pop();
            return value_;
        }
        Serial.println("Erreur, Pas de valeur à extraire");
        return nullptr;
    }

    bool hasValue() {
        return !list_queue.empty();
    }

    void onWrite(BLECharacteristic* pChar) override {
        std::string str_value = pChar->getValue();
        char* value_ = new char[str_value.length() + 1];
        strcpy(value_, str_value.c_str());

        list_queue.push(value_);
        
    }

    ~CharacteristicCallBack() {
        while (!list_queue.empty()) {
            delete[] list_queue.front();
            list_queue.pop();
        }
    }


};

class Characteristic {
private:
    std::string uuid;
    bool notify;
    bool write;
    bool read;
    BLECharacteristic* pCharacteristic;
    BLE2902* pBLE2902;
    BLEService* pService;
    CharacteristicCallBack* callback;



public:

    CharacteristicCallBack* getCallback() {
        return callback;
    };
    
    Characteristic(BLEServer* pServer, const std::string& uuidService_, const std::string& uuid_, const bool notify_ = true, const bool write_ = true, const bool read_ = true)
        : uuid(uuid_), notify(notify_), write(write_), read(read_) {

        pService = pServer->getServiceByUUID(uuidService_);

        Serial.print("Pointeur pService : 0x");
        Serial.println((size_t)pService, HEX);

        pCharacteristic = pService->createCharacteristic(
            uuid,
            BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE |
            BLECharacteristic::PROPERTY_NOTIFY
        );

        pBLE2902 = new BLE2902();
        pBLE2902->setNotifications(true);
        pCharacteristic->addDescriptor(pBLE2902);
        
        callback = new CharacteristicCallBack();
        pCharacteristic->setCallbacks(callback);

        pCharacteristic->setValue("nothing");
    }
};
