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
            server->listen();
            server->readMessage();
            if (server->hasMessage()) {
                logger::print(logger::INFO, "Message received : ", false);
                Serial.println(server->getMessage());
            }
        }
};