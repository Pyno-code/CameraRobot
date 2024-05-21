#include <bluetooth/bluetooth_controller.h>
#include <wifi/wifi_controller.h>
#include <wifi/server_controller.h>
#include <HardwareSerial.h>
#include <variable.cpp>


// Définir le nom du périphérique BLE
#define DEVICE_NAME "ESP32"

// Déclarer les instances des contrôleurs
BluetoothController* bleController;
WiFiController* wifiController;
ServerController* serverController;

bool variable::workingStatus;
bool variable::wifiConnectedStatus;
bool variable::bluetoothConnectedStatus;
bool variable::serverTcpConnectedStatus;

bool variable::orderWorking;
bool variable::orderWifiConnection;

bool variable::wifiInitialized;
bool variable::serverTcpInitialized;

String variable::ssid;
String variable::password;

String variable::ip;
int variable::port = 5000;

 

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

  if (variable::bluetoothConnectedStatus) {

    delay(1000); // attendre 1 seconde

  } else {
    // si j'ai l'ordre de m'arrêter ou si je ne suis pas connecté en bluetooth
    variable::wifiInitialized = false;
    variable::serverTcpInitialized = false;
    
    variable::workingStatus = false;
    variable::wifiConnectedStatus = false;
    variable::serverTcpConnectedStatus = false;
  }
}
