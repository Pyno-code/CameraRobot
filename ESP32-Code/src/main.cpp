#include <bluetooth/bluetooth_controller.h>
#include <wifi/wifi_controller.h>
#include <wifi/server_controller.h>
#include <HardwareSerial.h>
#include <variable.h>


// Définir le nom du périphérique BLE
#define DEVICE_NAME "ESP32"

// Déclarer les instances des contrôleurs
BluetoothController* bleController;
WiFiController* wifiController;
ServerController* serverController;


void setup() {
  Serial.begin(115200);
  
  delay(5000); // attendre que le moniteur série se connecte
  Serial.println("Hey working !");

  bleController = new BluetoothController(DEVICE_NAME);



  // initialiser les objets utilisant le wifi dans la loop ....
  // initialiser l'objet wifiController lors de l'envoie des données de connexion ....

}

void loop() {
  bleController->loop();

  if (variable::orderWorking && variable::bluetoothConnectedStatus) {
    // si j'ai l'ordre de marcher
    variable::workingStatus = true;

    if (variable::orderWifiConnection) {
      // si j'ai l'ordre de me connecter au wifi
      
      if (!variable::wifiInitialized) {
        // si le wifi n'est pas initialisé
        wifiController = new WiFiController();
        variable::wifiInitialized = true;
      }

      if (!wifiController->isConnected()) {
        // si le wifi n'est pas connecté
        bool connected = wifiController->connect(variable::ssid.c_str(), variable::password.c_str());
        variable::wifiConnectedStatus = connected;
      
        variable::serverTcpInitialized = false;
        variable::serverTcpConnectedStatus = false;

        if (connected) {
          variable::ip = wifiController->getLocalIP().toString();
        }

      } else {
        // si le wifi est connecté

        if (!variable::serverTcpInitialized) {
          // si le serveur tcp n'est pas initialisé

          serverController = new ServerController(variable::port);

          variable::serverTcpInitialized = true;
          variable::serverTcpConnectedStatus = true;
        }

        serverController->loop();
        
      } 
    } else {
      // si j'ai l'ordre de me déconnecter du wifi
      if (variable::wifiInitialized) {
        wifiController->disconnect();
        variable::wifiConnectedStatus = false;
        variable::wifiInitialized = false;
      }
    }

  } else {
    // si j'ai l'ordre de m'arrêter ou si je ne suis pas connecté en bluetooth
    variable::wifiInitialized = false;
    variable::serverTcpInitialized = false;
    
    variable::workingStatus = false;
    variable::wifiConnectedStatus = false;
    variable::serverTcpConnectedStatus = false;
  }
}
