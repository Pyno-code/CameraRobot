#include "wifi/server.h"
#include "logger.h"
#include <vector>

union FloatUnion {
    byte byteArray[4];
    float floatValue;
};

class ServerController {
    private:
        TcpServer* server;
        std::vector<std::array<float, 10>> *commandQueue;
    public:
        ServerController(int port, std::vector<std::array<float, 10>> *commandQueue_) {
            commandQueue = commandQueue_;
            server = new TcpServer(port);
            server->begin();
        }

        void loop() {

            server->listen();
            server->readMessage();

            if (server->hasMessage()) {
                int length = 0;
                byte* message = server->getMessage(length);
                // logger::print(logger::INFO, "Message received: ");
                // logger::print(logger::INFO, "length: ", false);
                // Serial.println(length);
                // Extract the last 16 bits from the message
                if (message && length == 2 + 24) { // 2 bytes for command + 24 bytes for 3 base64 encoded floats
                    // Process the first 16 bits (2 bytes)
                    uint16_t command = (message[0] << 8) | message[1];
                    // Serial.print("Command in binary: ");
                    // Serial.println(command, BIN);

                    // Decompose into 4-bit integers
                    uint8_t part1 = (command >> 12) & 0x0F;
                    uint8_t part2 = (command >> 8) & 0x0F;
                    uint8_t part3 = (command >> 4) & 0x0F;
                    uint8_t part4 = command & 0x0F;

                    // Convert each part into an int
                    float commandfloat1 = part1;
                    float commandfloat2 = part2;
                    float commandfloat3 = part3;
                    float commandfloat4 = part4;                    

                    // Print the converted integers
                    // Serial.print("Int 1: ");
                    // Serial.println(commandfloat1);
                    // Serial.print("Int 2: ");
                    // Serial.println(commandfloat2);
                    // Serial.print("Int 3: ");
                    // Serial.println(commandfloat3);
                    // Serial.print("Int 4: ");
                    // Serial.println(commandfloat4);

                    byte base64EncodedFloats[24];

                    for (int i = 0; i < 24; i++) {
                        base64EncodedFloats[i] = message[i + 2];
                    }
                    
                    FloatUnion float1;
                    FloatUnion float2;
                    FloatUnion float3;
                    FloatUnion float4;
                    FloatUnion float5;
                    FloatUnion float6;


                    for (int i = 0; i < 8; i++) {
                        float1.byteArray[i] = base64EncodedFloats[i];
                        float2.byteArray[i] = base64EncodedFloats[i + 4];
                        float3.byteArray[i] = base64EncodedFloats[i + 8];
                        float4.byteArray[i] = base64EncodedFloats[i + 12];
                        float5.byteArray[i] = base64EncodedFloats[i + 16];
                        float6.byteArray[i] = base64EncodedFloats[i + 20];
                    }

                    

                    // Serial.print("Arg 1: ");
                    // Serial.println(float1.floatValue);
                    // Serial.print("Arg 2: ");
                    // Serial.println(float2.floatValue);
                    // Serial.print("Arg 3: ");
                    // Serial.println(float3.floatValue);
                    // Serial.print("Arg 4: ");
                    // Serial.println(float4.floatValue);
                    // Serial.print("Arg 5: ");
                    // Serial.println(float5.floatValue);
                    // Serial.print("Arg 6: ");
                    // Serial.println(float6.floatValue);


                    std::array<float, 10> commandMessage = {commandfloat1, commandfloat2, commandfloat3, commandfloat4, float1.floatValue, float2.floatValue, float3.floatValue, float4.floatValue, float5.floatValue, float6.floatValue};
                    commandQueue->push_back(commandMessage);
                }
            }
            
        }

        ~ServerController() {
            delete server;
        }

        TcpServer* getServer() {
            return server;
        }

        void printBytesAsBinary(byte* message, int length) {
            for (int i = 0; i < length; i++) {
                for (int bit = 7; bit >= 0; bit--) {
                    Serial.print(bitRead(message[i], bit));
                }
                if (i < length - 1) {
                    // Serial.print(' ');
                }
            }
            Serial.println();
        }
};