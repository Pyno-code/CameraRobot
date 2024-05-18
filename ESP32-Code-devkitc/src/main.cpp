#include <bluetooth/bluetooth_controller.h>
#include <wifi/wifi_controller.h>
#include <wifi/server_controller.h>
#include <HardwareSerial.h>


// Définir le nom du périphérique BLE
#define DEVICE_NAME "ESP32"

// Déclarer les instances des contrôleurs
BluetoothController* bleController;
WiFiController* wifiController;
ServerController* serverController;

// Informations de connexion WiFi 
const char* ssid = "SFR_4B54";
const char* password = "sn3lb98lsgm9eqxu1k4m";
bool isInitialized = false;


void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  delay(5000); // attendre que le moniteur série se connecte
  Serial.println("Hey working !");
  // bleController = new BluetoothController(DEVICE_NAME);
  wifiController = new WiFiController();



  // initialiser les objets utilisant le wifi dans la loop ....
  // initialiser l'objet wifiController lors de l'envoie des données de connexion ....

}

void loop() {
  if (!wifiController->isConnected()) {
      delay(1000);
      wifiController->connect(ssid, password);
      isInitialized = false;

  } else {
    if (!isInitialized) {
      serverController = new ServerController(5000);
      isInitialized = true;
    }
    else {
      serverController->loop();
    }
  }
}
