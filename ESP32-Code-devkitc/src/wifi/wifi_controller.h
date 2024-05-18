#include <WiFi.h>

class WiFiController {
    
    private:
        int maxRetries;
        int timeConnection = 0;
    public:

        WiFiController(int maxRetries_=10) {
            maxRetries = maxRetries_;
        }

        bool connect(const char* ssid, const char* password) {
            Serial.println("WiFi not connected, connect...");
            WiFi.begin(ssid, password);
            int retries = 0;
            while (retries < maxRetries)
            {
                Serial.print(".");

                if (isConnected()) {
                    Serial.println();
                    Serial.println("Connected to the WiFi network");
                    Serial.print("IP Address: ");
                    Serial.println(WiFi.localIP());
                    return true;
                }
                delay(1000);
                retries += 1;
            }
            Serial.println();
            Serial.println("Failed to connect to the WiFi network");
            return false;            
        }
        

        void disconnect() {
            WiFi.disconnect();
            Serial.println("Disconnected from WiFi");
        }

        IPAddress getLocalIP() {
            return WiFi.localIP();
        }

        bool isConnected() {
            return WiFi.status() == WL_CONNECTED;
        }

};