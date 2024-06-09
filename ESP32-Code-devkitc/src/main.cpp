#include <controller.cpp>
#include "logger.h"

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
String variable::macAddress = "XX:XX:XX:XX:XX:XX";


Controller* controller;


void setup() {
  controller = new Controller();
  controller->setup();
}

void loop() {
  unsigned long start_time = millis();
  controller->loop();
  unsigned long time_elasped = millis() - start_time;
  if (time_elasped > 50) {
    // logger::print(logger::DEBUG, "Loop time : ", false);
    // Serial.println(String(millis() - start_time));
  }
}
