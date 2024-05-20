#include <WiFi.h>

class WiFiController {
    
    private:
        int maxRetries;
        int timeConnection = 0;
    public:

        WiFiController(int maxRetries_=10) {
            WiFi.mode(WIFI_STA);
            maxRetries = maxRetries_;
        }

        bool connect(const char* ssid, const char* password) {
            WiFi.begin(ssid, password);
            int retries = 0;
            while (retries < maxRetries)
            {
                if (isConnected()) {
                    return true;
                }
                delay(1000);
                retries += 1;
            }
            Serial.println();
            return false;
        }
        

        void disconnect() {
            WiFi.disconnect();
        }

        IPAddress getLocalIP() {
            return WiFi.localIP();
        }

        bool isConnected() {
            return WiFi.status() == WL_CONNECTED;
        }

};