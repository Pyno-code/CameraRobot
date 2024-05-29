#include <Arduino.h>


namespace variable {
    extern bool workingStatus;
    extern bool wifiConnectedStatus;
    extern bool bluetoothConnectedStatus;
    extern bool serverTcpConnectedStatus;
    
    extern bool orderWorking;
    extern bool orderWifiConnection;
    extern bool orderTCPConnection;
    
    extern bool wifiInitialized;
    extern bool serverTcpInitialized;

    extern String ssid;
    extern String password;

    extern String ip;
    extern int port;

    extern String macAddress;
}

