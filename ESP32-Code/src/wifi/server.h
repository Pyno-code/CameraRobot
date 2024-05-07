#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <Vector.h>

class TcpClient : public WiFiClient {
    public:
        TcpClient(const WiFiClient& client) : WiFiClient(client) {}

    private:
        Vector<String> messageQueue;

    public:
        void addMessage(const String& message) {
            messageQueue.push_back(message);
        }

        String popMessage() {
            if (!messageQueue.empty()) {
                String message = messageQueue.front();
                messageQueue.remove(0);
                return message;
            }
            return "";
        }

        void clearMessages() {
            messageQueue.clear();
        }

        bool hasMessages() {
            return !messageQueue.empty();
        }
};

class TcpServer {
    private:
        WiFiServer server;
        Vector<TcpClient> clients;
        bool isRunning = false;
        int port;

    public:
        TcpServer(int port_) : port(port_), server(port_) {}

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
            TcpClient newClient(server.available());
            if (newClient) {
                clients.push_back(newClient);
                //TcpClient client = clients.back();
                Serial.print("Client connected from IP: ");
                Serial.println(newClient.remoteIP());
                Serial.print("Client connected from port: ");
                Serial.println(newClient.remotePort());
                Serial.println("New client connected to the TCP server");
                Serial.print("Number of clients connected: ");
                Serial.println(clients.size());
            }
        }

        void kickClient(int clientIndex) {
            if (clientIndex >= 0 && clientIndex < clients.size()) {
                clients[clientIndex].stop();
                clients.remove(clientIndex);
                Serial.println("Client kicked");

            }
        }

        void readMessages() {
            for (int i = 0; i < clients.size(); i++) {
                // check si il y a des messages à lire
                if (clients[i].available()) {
                    Serial.print("Reading message from client ");
                    String message = clients[i].readString();
                    // lis jusqu'à la fin de la ligne
                    Serial.print("Received message from client ");
                    Serial.print(i);
                    Serial.print(": ");
                    Serial.println(message);
                }
            }
        }

        void sendMessage(int clientIndex, const String& message) {
            if (clientIndex >= 0 && clientIndex < clients.size()) {
                clients[clientIndex].println(message);
                Serial.print("Sent message to client ");
                Serial.print(clientIndex);
                Serial.print(": ");
                Serial.println(message);
            }
        }

        void stopServer() {
            for (int i = 0; i < clients.size(); i++) {
                kickClient(i);
            }
            server.stop();
            isRunning = false;
            Serial.println("Server stopped");
        }

        bool isAvailable() {
            return isRunning;
        }

        bool hasClients() {
            return clients.size() > 0;
        }

        Vector<TcpClient>& getClients() {
            return clients;
        }
};