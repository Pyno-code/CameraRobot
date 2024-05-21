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
    
    Serial.println("Bluetooth connected");
    delay(10000);

  } else {
    // si j'ai l'ordre de m'arrêter ou si je ne suis pas connecté en bluetooth
    variable::wifiInitialized = false;
    variable::serverTcpInitialized = false;
    
    variable::workingStatus = false;
    variable::wifiConnectedStatus = false;
    variable::serverTcpConnectedStatus = false;
  }
}
