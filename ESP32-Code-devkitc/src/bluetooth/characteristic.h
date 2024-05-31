#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <stdio.h>
#include <string.h>
#include <queue>
#include <LinkedList.h>



class CharacteristicCallBack : public BLECharacteristicCallbacks {
private:
    LinkedList<String> messageQueue = LinkedList<String>();

public:
    String popMessage() {
        if (hasValue()) {
            String message = messageQueue.pop();
            return message;
        }
        else {
            return "";
        }
    }

    void clearQueue() {
        messageQueue.clear();
    }

    bool hasValue() {
        return (messageQueue.size() != 0);
    }

    void onWrite(BLECharacteristic* pChar) override {
        std::string str_value = pChar->getValue();
        String message = String(str_value.c_str());
        messageQueue.add(message);
    }

    ~CharacteristicCallBack() {
        delete &messageQueue;
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
            pCharacteristic->setValue("");

        }

        bool hasValue() {
            return callback->hasValue();
        }

        String getMessage() {
            return callback->popMessage();
        }

        void setValue(const String value) {
            callback->clearQueue();
            pCharacteristic->setValue(std::string(value.c_str()));
        }

        String getCurrentValue() {
            return String(pCharacteristic->getValue().c_str());
        }
};
