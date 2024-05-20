#include "wifi/server.h"


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
                Serial.print("Message received : ");
                Serial.println(server->getMessage());
            }
        }
};