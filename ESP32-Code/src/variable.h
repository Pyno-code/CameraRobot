#include <Arduino.h>


namespace variable {
    bool workingStatus;
    bool wifiConnectedStatus;
    bool bluetoothConnectedStatus;
    bool serverTcpConnectedStatus;
    
    bool orderWorking;
    bool orderWifiConnection;
    
    bool wifiInitialized;
    bool serverTcpInitialized;

    String ssid;
    String password;

    String ip;
    const int port = 5000;
}

