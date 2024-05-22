#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <HardwareSerial.h>
#include "bluetooth/characteristic.h"
#include "bluetooth/server.h"
#include "variable.cpp"


#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"


class BluetoothController {
    private:
        ServerBluetooth *pServerBluetooth;
        bool isRunning = false;
        std::map<std::string, Characteristic*> characteristics;

        //************************************************************
        #define SSID_UUID "02456daf-2ff7-431b-812b-772f0eb7b2b2"
        #define PASSWORD_UUID "ebac488a-1cd1-4bdf-b6a6-9fc78fe75772"

        #define IP_UUID "02f211b0-37e2-4dcf-a57c-93d6c26bb79f"
        #define PORT_UUID "0f2824b0-0572-4dae-b615-360d0064f176"

        #define WIFI_STATUS_UUID "a5de0af1-459d-428b-9f02-be1a127d5ae2"
        #define WORKING_STATUS_UUID "3c21be21-7cd9-467b-8ccf-58582b6fe86c"
        #define SERVER_TCP_STATUS_UUID "09366094-9e6d-45ed-9a5e-d6da66e366fa"

        #define ORDER_WIFI_CONNECTION_UUID "60a8d493-3283-404b-8a99-7523a7f8dbc6"
        #define ORDER_WORKING_UUID "40265fbb-1001-4675-b93f-1e2c618e066b"
        //************************************************************
        
    public:
        BluetoothController(std::string deviceName) {
            Serial.println("Initializing Bluetooth Controller");
            BLEDevice::init(deviceName);


            // definier tout les UUID ici
            // https://www.uuidgenerator.net/

           
            // fin des définitions des UUID
            Serial.println("Initializing bluetooth server ...");
            pServerBluetooth = new ServerBluetooth(deviceName, SERVICE_UUID);
            Serial.println("Bluetooth Server initialized");
            //cré les caractéristiques et ensuite start le serveur
            
            //toutes les charactéristiques doivent être créées ici
            
            //toutes les charactéristiques enregistre des Strings (String)

            //************************************************************
            Characteristic ssidCharacteristic = *createCharacteristic(SSID_UUID);
            Characteristic passwordCharacteristic = *createCharacteristic(PASSWORD_UUID);
            Characteristic ipCharacteristic = *createCharacteristic(IP_UUID);
            Characteristic portCharacteristic = *createCharacteristic(PORT_UUID);

            Characteristic workingStatusCharacteristic = *createCharacteristic(WORKING_STATUS_UUID);
            Characteristic wifiStatusCharacteristic = *createCharacteristic(WIFI_STATUS_UUID);
            Characteristic serverTcpStatusCharacteristic = *createCharacteristic(SERVER_TCP_STATUS_UUID);

            Characteristic orderConnectionWifiCharacteristic = *createCharacteristic(ORDER_WIFI_CONNECTION_UUID);
            Characteristic orderWorkingCharacteristic = *createCharacteristic(ORDER_WORKING_UUID);
            //************************************************************
            pServerBluetooth->startServer();
            Serial.println("Bluetooth Controller initialized");
            
        }

        
        // Cette fonction est un exemple de l'utilisation du contrôleur, elle ne doit pas être appelée.
        void loop() {
            if (!pServerBluetooth->isDeviceConnected()) {
                variable::bluetoothConnectedStatus = false;
                
                Serial.println("ERROR ->");
                pServerBluetooth->startAdvertising();
                Serial.println("<- ERROR");

                delay(2000);
                if (pServerBluetooth->isDeviceConnected()) {
                    variable::bluetoothConnectedStatus = true;
                }

            } else {
                
                
                // lire les valeurs et les ordres ici

                // ordre de marcher
                if ((characteristics)[ORDER_WORKING_UUID]->hasValue()) {
                    String orderWorking = (characteristics)[ORDER_WORKING_UUID]->getMessage();
                    variable::orderWorking = stringToBool(orderWorking);
                    Serial.println("Order working : " + orderWorking);
                }


                // ordre de connexion wifi
                if ((characteristics)[ORDER_WIFI_CONNECTION_UUID]->hasValue()) {
                    String orderWifiConnection = (characteristics)[ORDER_WIFI_CONNECTION_UUID]->getMessage();
                    variable::orderWifiConnection = stringToBool(orderWifiConnection);
                    Serial.println("Order wifi connection : " + orderWifiConnection);
                }
                

                // valeur de ssid
                if ((characteristics)[SSID_UUID]->hasValue()) {
                    variable::ssid = (characteristics)[SSID_UUID]->getMessage();
                    Serial.println("SSID : " + variable::ssid);
                }
                

                // valeur de password
                if ((characteristics)[PASSWORD_UUID]->hasValue()) {
                    variable::password = (characteristics)[PASSWORD_UUID]->getMessage();
                    Serial.println("Password : " + variable::password);
                }

                // écrire les status si la valeur a changé

                // status de connexion bluetooth
                if (variable::wifiConnectedStatus != stringToBool((characteristics)[WIFI_STATUS_UUID]->getCurrentValue())) {
                    (characteristics)[WIFI_STATUS_UUID]->setValue(boolToString(variable::wifiConnectedStatus));
                    Serial.println("Wifi status : " + boolToString(variable::wifiConnectedStatus));
                }

                
                // status de connexion wifi
                if (variable::workingStatus != stringToBool((characteristics)[WORKING_STATUS_UUID]->getCurrentValue())) {
                    (characteristics)[WORKING_STATUS_UUID]->setValue(boolToString(variable::workingStatus));
                    Serial.println("Working status : " + boolToString(variable::workingStatus));
                }


                // status de connexion serveur tcp
                if (variable::serverTcpConnectedStatus != stringToBool((characteristics)[SERVER_TCP_STATUS_UUID]->getCurrentValue())) {
                    (characteristics)[SERVER_TCP_STATUS_UUID]->setValue(boolToString(variable::serverTcpConnectedStatus));
                    Serial.println("Server tcp status : " + boolToString(variable::serverTcpConnectedStatus));
                }


                // écriture de l'ip
                if (variable::ip != (characteristics)[IP_UUID]->getCurrentValue()) {
                    (characteristics)[IP_UUID]->setValue(variable::ip);
                    Serial.println("IP : " + variable::ip);
                }


                // écriture du port
                if (variable::port != (characteristics)[PORT_UUID]->getCurrentValue().toInt()) {
                    (characteristics)[PORT_UUID]->setValue(String(variable::port));
                    Serial.println("Port : " + String(variable::port));
                }
            }
        }

        Characteristic* createCharacteristic(const char* uuid) {
            Characteristic *characteristic = new Characteristic(pServerBluetooth->getServer(), SERVICE_UUID, uuid);
            (characteristics)[uuid] = characteristic;
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


        void stop() {
            pServerBluetooth->stopServer();
            characteristics.clear();
            delete pServerBluetooth;
            isRunning = false;
        }

        bool hasStoped() {
            return !isRunning;
        }

        Characteristic* getCharacteristic(const char* uuid) {
            return (characteristics)[uuid];
        }

        bool stringToBool(String str) {
            return str == "true";
        }

        String boolToString(bool value) {
            return value ? "true" : "false";
        }

        ~BluetoothController() {
            if (isRunning) {
                stop();
            }
        }
};
