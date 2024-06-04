#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <LinkedList.h>
#include "logger.h"

class TcpClient : public WiFiClient {

    private:
        LinkedList<byte*> messageQueue;
        LinkedList<int> messageLengths;

    public:
        TcpClient() : WiFiClient() {}
        TcpClient(const WiFiClient& client) : WiFiClient(client) {}

        ~TcpClient() {
            clearMessages();
        }

        void addMessage(byte* message, int length) {
            byte* messageCopy = new byte[length];
            memcpy(messageCopy, message, length);
            messageQueue.add(messageCopy);
            messageLengths.add(length);
        }

        byte* popMessage(int &length) {
            if (hasMessage()) {
                byte* message = messageQueue.get(0);
                length = messageLengths.get(0);
                messageQueue.remove(0);
                messageLengths.remove(0);
                return message;
            }
            length = 0;
            return nullptr;
        }

        void clearMessages() {
            while (hasMessage()) {
                int length;
                byte* message = popMessage(length);
                delete[] message;
            }
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
        TcpServer(int port_) : port(port_), server(port_) {}

        void begin() {
            server.begin();
            isRunning = true;
            server.setNoDelay(true);
            logger::print(logger::INFO, "Server started at: ", false);
            Serial.print(WiFi.localIP());
            Serial.print(":");
            Serial.println(port);
            logger::print(logger::INFO, "Listening for clients... (in future loop)");
        }

        void listen() {
            if (!client.connected()) {
                delay(1000);
                TcpClient newClient(server.available());
                if (newClient) {
                    client = newClient;
                    logger::print(logger::INFO, "New client connected: ", false);
                    Serial.println(client.remoteIP());
                }
            }
        }

        void kickClient() {
            client.stop();
        }

        void readMessage() {   
            const int bufferSize = 26;
            byte buffer[bufferSize];

            if (client.available()) {
                int bytesRead = client.readBytes(buffer, bufferSize);
                if (bytesRead > 0) {
                    client.addMessage(buffer, bytesRead);
                }
            }
        }

        byte* getMessage(int& length) {
            return client.popMessage(length);
        }

        bool hasMessage() {
            return client.hasMessage();
        }

        void sendMessage(const String& message) {
            client.print(message);
            logger::print(logger::INFO, "Sent message to client ", false);
            Serial.print(": ");
            Serial.println(message);
        }

        void stopServer() {
            kickClient();
            server.stop();
            isRunning = false;
            logger::print(logger::INFO, "Server stopped");
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

        bool isConnected() {
            return isRunning;
        }
};