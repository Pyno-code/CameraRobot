#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <Vector.h>
#include <LinkedList.h>



class TcpClient : public WiFiClient {

    private:
        LinkedList<String> messageQueue = LinkedList<String>();

    public:
        TcpClient() : WiFiClient() {}
        TcpClient(const WiFiClient& client) : WiFiClient(client) {}

        void addMessage(const String& message) {
            messageQueue.add(message);
        }

        String popMessage() {
            if (hasMessage()) {
                String message = messageQueue.pop();
                messageQueue.remove(0);
                return message;
            }
            return "";
        }

        void clearMessages() {
            messageQueue.clear();
        }

        bool hasMessage() {
            return (messageQueue.size() != 0);
        }

};

class TcpServer {
    private:
        TcpClient client;
        bool isRunning = false;
            int port;

        public:
            WiFiServer server;
            TcpServer(int port_) : port(port_) {
                server = WiFiServer(port);
            }


        void begin() {
            server.begin();
            isRunning = true;
            server.setNoDelay(true);
            Serial.print("Server started at : ");
            Serial.print(WiFi.localIP());
            Serial.print(":");
            Serial.println(port);


        }

        void listen() {
            if (!client.connected()) {
                delay(1000);
                Serial.println("Listening for clients...");
                TcpClient newClient(server.available());
                if (newClient) {
                    client = newClient;
                }
            }
        }

        void kickClient() {
            client.stop();
        }

        void readMessage() {
            if (client.available()) {
                String message = client.readStringUntil('$');
                client.addMessage(message);
            }
        }

        String getMessage() {
            return client.popMessage();
        }

        bool hasMessage() {
            return client.hasMessage();
        }

        void sendMessage(const String& message) {
            client.print(message);
            Serial.print("Sent message to client ");
            Serial.print(": ");
            Serial.println(message);
        }

        void stopServer() {
            
            kickClient();

            server.stop();
            isRunning = false;
            Serial.println("Server stopped");
        }

        bool isAvailable() {
            return isRunning;
        }

        bool hasClients() {
            return client.connected();
        }

        TcpClient getClient() {
            return client;
        }
};