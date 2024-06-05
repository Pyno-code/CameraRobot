#include <bluetooth/bluetooth_controller.h>
#include <wifi/wifi_controller.h>
#include <wifi/server_controller.h>
#include <HardwareSerial.h>
#include <variable.cpp>
#include "logger.h"
#include "motor/motor_controller.h"


class Controller {
    private:
        BluetoothController* bleController;
        WiFiController* wifiController;
        ServerController* serverController;
        MotorController* motorController;

        std::vector<std::array<float, 10>> *commandQueue;
        

        const std::string DEVICE_NAME = "ESP32";
    public:

        Controller() {
            commandQueue = new std::vector<std::array<float, 10>>();
        }

        void setup() {
            Serial.begin(115200);

            logger::print(logger::INFO, "Hey working !");

            bleController = new BluetoothController(DEVICE_NAME);
            // motorController = new MotorController(commandQueue);
            motorController = new MotorController(commandQueue);

            // initialiser les objets utilisant le wifi dans la loop ....
        }

        void loop() {
            
            bleController->loop();
            // motorController->loop(commandQueue);
            motorController->loop();

            

            if (variable::bluetoothConnectedStatus && variable::orderWorking) {

                // ordre de marcher
                variable::workingStatus = true;

                if (variable::orderWifiConnection) {
                    // si j'ai l'ordre de me connecter au wifi
                    if (!variable::wifiInitialized) {
                        initializeWifi();
                    }

                    if (!wifiController->isConnected()) {
                        orderWifiConnection();
                    } else {

                        if (variable::orderTCPConnection) {
                        // si j'ai l'ordre de me connecter au serveur tcp

                            if (!variable::serverTcpInitialized) {
                                // si le serveur tcp n'est pas initialisé
                                initializeTCPServer();
                            } else {
                                // si le serveur tcp est initialisé et que j'ai l'ordre de me connecter
                                serverController->loop();  
                            }

                        } else {
                            // si je n'ai pas l'ordre de me connecter au serveur tcp
                            stopTCPConnection();
                        }

                    }    
                } else {
                    // si je n'ai pas l'ordre de me connecter au wifi
                    stopTCPConnection();
                    stopWifiConnection();
                }

            } else {
                // ordre de s'arrêter
                stopTCPConnection();
                stopWifiConnection();
                stopWorking();
            }

        }

        void initializeWifi() {
            if (!variable::wifiInitialized) {
                // si le wifi n'est pas initialisé
                wifiController = new WiFiController();

                variable::wifiInitialized = true;
                variable::wifiConnectedStatus = false;

                logger::print(logger::INFO, "Wifi initialized");
            }
        }

        void orderWifiConnection() {
            // si le wifi n'est pas connecté
            logger::print(logger::INFO, "Trying to connect to the Wifi : ");
            Serial.print("  SSID : ");
            Serial.println(variable::ssid);
            Serial.print("  PASSWORD : ");
            Serial.println(variable::password);
            bool connected = wifiController->connect(variable::ssid.c_str(), variable::password.c_str());
            
            if (connected) {
                // si le wifi est connecté
                logger::print(logger::INFO, "Wifi connected");
                variable::macAddress = wifiController->getMacAddress();
                variable::wifiConnectedStatus = true;
                variable::ip = wifiController->getLocalIP().toString();
            }
        }

        void initializeTCPServer() {
            serverController = new ServerController(variable::port, commandQueue);
            variable::serverTcpInitialized = true;
            variable::serverTcpConnectedStatus = true;
            logger::print(logger::INFO, "Server tcp initialized");
        }


        void stopWorking() {
            variable::workingStatus = false;
        }

        void stopWifiConnection() {
            if (variable::wifiInitialized) {

                if (wifiController->isConnected()) {
                    wifiController->disconnect();
                    delete wifiController;
                    variable::wifiConnectedStatus = false;
                    variable::wifiInitialized = false;
                    logger::print(logger::INFO, "Wifi disconnected");
                }
            }
        }

        void stopTCPConnection() {
            if (variable::serverTcpInitialized) {
                if (serverController->getServer()->isConnected()) {
                    serverController->getServer()->stopServer();
                    delete serverController;
                    variable::serverTcpConnectedStatus = false;
                    variable::serverTcpInitialized = false;
                    logger::print(logger::INFO, "Server tcp disconnected");
                }
            }
        }
};