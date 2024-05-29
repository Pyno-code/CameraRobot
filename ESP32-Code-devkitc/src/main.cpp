#include <bluetooth/bluetooth_controller.h>
#include <wifi/wifi_controller.h>
#include <wifi/server_controller.h>
#include <HardwareSerial.h>
#include <variable.cpp>
#include "logger.h"



// Définir le nom du périphérique BLE
#define DEVICE_NAME "ESP32"

// Déclarer les instances des contrôleurs
BluetoothController* bleController;
WiFiController* wifiController;
ServerController* serverController;

bool variable::workingStatus = false;
bool variable::wifiConnectedStatus = false;
bool variable::bluetoothConnectedStatus = false;
bool variable::serverTcpConnectedStatus = false;

bool variable::orderWorking = false;
bool variable::orderWifiConnection = false;
bool variable::orderTCPConnection = false;

bool variable::wifiInitialized = false;
bool variable::serverTcpInitialized = false;

String variable::ssid;
String variable::password;

String variable::ip;
int variable::port = 5000;
String variable::macAddress = "00:00:00:00:00:00";



void setup() {
  Serial.begin(115200);

  delay(5000); // attendre que le moniteur série se connecte
  logger::print(logger::INFO, "Hey working !");

  bleController = new BluetoothController(DEVICE_NAME);

  // initialiser les objets utilisant le wifi dans la loop ....
  // initialiser l'objet wifiController lors de l'envoie des données de connexion ....

}

void loop() {
  
  bleController->loop();

  if (variable::bluetoothConnectedStatus && variable::orderWorking) {


    // ordre de marcher
    variable::workingStatus = true;

    if (variable::orderWifiConnection) {
    // si j'ai l'ordre de me connecter au wifi
      if (!variable::wifiInitialized) {
        // si le wifi n'est pas initialisé
        wifiController = new WiFiController();

        variable::wifiInitialized = true;
        variable::wifiConnectedStatus = false;
        variable::serverTcpInitialized = false;
        variable::serverTcpConnectedStatus = false;

        logger::print(logger::INFO, "Wifi initialized");
      }

      if (!wifiController->isConnected()) {
        variable::wifiConnectedStatus = false;
        variable::serverTcpInitialized = false;
        variable::serverTcpConnectedStatus = false;

        // si le wifi n'est pas connecté
        bool connected = wifiController->connect(variable::ssid.c_str(), variable::password.c_str());
      
        if (connected) {
          // si le wifi est connecté
          logger::print(logger::INFO, "Wifi connected");
          variable::macAddress = wifiController->getMacAddress();
          variable::wifiConnectedStatus = true;
          variable::ip = wifiController->getLocalIP().toString();
        }
      } else {

        if (variable::orderTCPConnection) {
          // si j'ai l'ordre de me connecter au serveur tcp

          if (!variable::serverTcpInitialized) {
            // si le serveur tcp n'est pas initialisé
            serverController = new ServerController(variable::port);
            variable::serverTcpInitialized = true;
            variable::serverTcpConnectedStatus = true;
            logger::print(logger::INFO, "Server tcp initialized");
          } else {
            serverController->loop();
          }
        } else {
          // si je n'ai pas l'ordre de me connecter au serveur tcp

          if (variable::serverTcpInitialized) {
            // si le serveur tcp est initialisé

            if (serverController->getServer()->isConnected()) {
              serverController->getServer()->stopServer();
              variable::serverTcpConnectedStatus = false;
              variable::serverTcpInitialized = false;
              logger::print(logger::INFO, "Server tcp disconnected");
            }


          }
        }

      }    
    } else {
      if (variable::wifiInitialized) {
        if (wifiController->isConnected()) {
          wifiController->disconnect();
          variable::wifiConnectedStatus = false;
          variable::wifiInitialized = false;
          logger::print(logger::INFO, "Wifi disconnected");
        }
      }
    }

  } else {
    // ordre de s'arrêter
    variable::workingStatus = false;
    variable::wifiConnectedStatus = false;
    variable::serverTcpConnectedStatus = false;

    variable::wifiInitialized = false;
    variable::serverTcpInitialized = false;

    variable::orderWifiConnection = false;
    variable::orderWorking = false;
    variable::orderTCPConnection = false;
  }
}
