#include <controller.cpp>

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


Controller* controller;


void setup() {
  controller = new Controller();
  controller->setup();
}

void loop() {
  controller->loop();
}
