#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID_ACTION_CONNECT_TO_WIFI "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHARACTERISTIC_UUID_SSID "d7be7b90-2423-4d6e-926d-239bc96bb2fd"
#define CHARACTERISTIC_UUID_WIFI_PASSWORD "47524f89-07c8-43b6-bf06-a21c77bfdee8"
#define CHARACTERISTIC_UUID_CONNECTED_TO_WIFI "f13163b4-cc7f-456b-9ea4-5c6d9cec8ee3"


BLECharacteristic* pCharacteristic_action_connect_to_wifi = NULL;
BLECharacteristic* pCharacteristic_ssid = NULL;
BLECharacteristic* pCharacteristic_wifi_password = NULL;
BLECharacteristic* pCharacteristic_connected_to_wifi = NULL;
