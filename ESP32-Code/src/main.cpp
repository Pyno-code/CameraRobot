#include "bluetooth/bluetooth_controller.h"
#include "wifi/wifi_controller.h"
#include <wifi/server.h>
#include <HardwareSerial.h>

// Définir le nom du périphérique BLE
#define DEVICE_NAME "ESP32"

// Déclarer une instance de BluetoothController
BluetoothController* bleController;
WiFiController* wifiController;
TcpServer* serverWiFi;


void connect_to_wifi() {
  if (!wifiController->isConnected()) {
    wifiController->connect("test", "12345678");
    
    if (wifiController->isConnected()) {
      Serial.println("Connected to the WiFi network"); 
      Serial.print("Local ESP32 IP: ");
      Serial.println(wifiController->getLocalIP());
    }
  }
}

void setup() {

  Serial.begin(115200);
  Serial.println("Hey working !"); 

  // initialiser les objets ici : 
  // bleController = new BluetoothController(DEVICE_NAME);
  wifiController = new WiFiController();
  connect_to_wifi();

  if (wifiController->isConnected()) {
    serverWiFi = new TcpServer(5000);
    serverWiFi->begin();
  }
  else {
    Serial.println("Failed to connect to the WiFi network");
  }

}

void loop() {
  // Appeler la méthode loop de BluetoothController
  // bleController->loop();

  if (wifiController->isConnected()) {
    serverWiFi->listen();
    // Serial.print(serverWiFi->hasClients());
    if (serverWiFi->hasClients()) {
      Serial.println("Client connected");
      serverWiFi->readMessages();
      TcpClient client = serverWiFi->getClients()[0];
      if (client.hasMessages()) {
        Serial.println(client.popMessage());
      }
    }
  }
  else {
    connect_to_wifi();
  }
}
