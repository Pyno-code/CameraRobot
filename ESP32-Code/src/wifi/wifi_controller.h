#include <WiFi.h>

class WiFiController {
    
    private:
        int maxRetries;
        int timeout; // milliseconds
    public:

        WiFiController(int maxRetries_=10, int timeout_=4000) {
            maxRetries = maxRetries_;
            timeout = timeout_;
        }

        bool connect(const char* ssid, const char* password) {
            int retries = 0;
            unsigned long startTime = millis();

            while (retries < maxRetries && (millis() - startTime) < timeout) {
                WiFi.begin(ssid, password);
                Serial.println("Connecting to WiFi");
                delay(1000);

                if (WiFi.status() == WL_CONNECTED) {
                    Serial.println("Connected to WiFi");
                    return true;
                }
                retries++;
            }

            Serial.println("Failed to connect to WiFi");
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