#include "wifi/server.h"
#include "logger.h"


class ServerController {
    private:
        TcpServer* server;
    
    public:
        ServerController(int port) {
            server = new TcpServer(port);
            server->begin();
        }

        void loop() {
            // implementer de la logique ici
            // TODO : pb icic

            server->listen();

            server->readMessage();

            if (server->hasMessage()) {
                String message = server->getMessage();
                // server->sendMessage("Message received");
                // Split the message into parts based on the delimiter '|'

                std::vector<std::string> command = parseMessage(message.c_str());

                if (command[0] == "ping") {
                    logger::print(logger::INFO, "Ping received");
                    server->sendMessage(message);
                } else {
                    logger::print(logger::INFO, "Message received : ", false);
                    Serial.println(message);
                }
                
                
            }
            
        }

        ~ServerController() {
            delete server;
        }

        TcpServer* getServer() {
            return server;
        }

        std::vector<std::string> parseMessage(std::string message) {
            std::vector<std::string> parts;
            std::string delimiter = "|";
            size_t pos = 0;
            std::string token;
            while ((pos = message.find(delimiter)) != std::string::npos) {
                token = message.substr(0, pos);
                parts.push_back(token);
                message.erase(0, pos + delimiter.length());
            }
            // Add the last part of the message
            parts.push_back(message);
            return parts;
        }
};