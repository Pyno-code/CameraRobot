#include <FastAccelStepper.h>
#include <motor/motor.h>
#include <logger.h>
#include <map>
#include <string>
#include <iostream>
#include <vector>


#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_MID  7
#define DIR_PIN_MID   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4

// Constants
#define STATUS  0
#define PING  1
#define MOTOR  2
#define POSITION  3

#define GET 1
#define SET  2
#define STOP  3
#define START  4
#define SHUTDOWN  5

#define ANGLE  6
#define SPEED  7

#define ALL 1
#define MOTOR_BASE 2
#define MOTOR_MIDDLE  3
#define MOTOR_TOP  4
#define MOTOR_X  5
#define MOTOR_Y  6
#define MOTOR_Z  7

// // List of arguments

// std::vector<std::map<std::string, int>> LIST_ARGS = {
//     {
//         {"STATUS", STATUS},
//         {"PING", PING},
//         {"MOTOR", MOTOR},
//         {"POSITION", POSITION}
//     },
//     {
//         {"GET", GET},
//         {"SET", SET},
//         {"STOP", STOP},
//         {"START", START},
//         {"SHUTDOWN", SHUTDOWN},
//         {"ANGLE", ANGLE},
//         {"SPEED", SPEED}
//     },
//     {
//         {"ANGLE", SPEED},
//         {"SPEED", ANGLE}
//     },
//     {
//         {"ALL", ALL},
//         {"MOTOR_BASE", MOTOR_BASE},
//         {"MOTOR_MIDDLE", MOTOR_MIDDLE},
//         {"MOTOR_TOP", MOTOR_TOP},
//         {"MOTOR_X", MOTOR_X},
//         {"MOTOR_Y", MOTOR_Y},
//         {"MOTOR_Z", MOTOR_Z}
//     }
// };


class MotorController {
    private:
        Motor* stepper_base;
        Motor* stepper_middle;
        Motor* stepper_top;
        std::vector<std::array<float, 10>>* commandQueue;
        FastAccelStepperEngine engine;

        
    public:
        MotorController(std::vector<std::array<float, 10>> *commandQueue_) {
            engine = FastAccelStepperEngine();
            engine.init();
            commandQueue = commandQueue_;
            stepper_base = new Motor(engine, MOTOR_BASE, STEP_PIN_BASE, DIR_PIN_BASE, 200);
            stepper_middle = new Motor(engine, MOTOR_MIDDLE, STEP_PIN_MID, DIR_PIN_MID, 200);
            stepper_top = new Motor(engine, MOTOR_TOP, STEP_PIN_TOP, DIR_PIN_TOP, 800);
            Serial.println("Motor Controller initialized");
        }

        void loop() {
            if (commandQueue->size() > 0) {
                

                std::array<float, 10> command = (*commandQueue)[0];
                logger::print(logger::INFO, "Command received: ", false);
                for (int i = 0; i < command.size(); i++) {
                    Serial.print(command[i]);
                    Serial.print(" ");
                }
                Serial.println();
                commandQueue->erase(commandQueue->begin());
                

                if (command[0] == MOTOR) {
                    Serial.println("MOTOR Command");
                    int motor_id = (int) (command[3]);
                    // logger::print(logger::INFO, "Motor id : ", false);
                    // Serial.println(motor_id);

                    if (motor_id != ALL and motor_id != STATUS) {
                        Motor* motor;
                        if (motor_id == MOTOR_BASE) {
                            Serial.print("  MOTOR_BASE");
                            motor = stepper_base;
                        } else if (motor_id == MOTOR_MIDDLE) {
                            Serial.print("  MOTOR_MIDDLE");
                            motor = stepper_middle;

                        } else if (motor_id == MOTOR_TOP) {
                            Serial.print("  MOTOR_TOP");
                            motor = stepper_top;
                        }
                        Serial.print(" | id : ");
                        Serial.print(motor->getID());
                        Serial.println();

                        if (command[1] == SET) {
                            Serial.println("    SET Command : ");
                            if (command[2] == ANGLE) {
                                Serial.print("      ANGLE Command : ");
                                motor->moveAngle(command[4]);
                            } else if (command[2] == SPEED) {
                                Serial.print("      SPEED Command : ");
                                motor->setSpeed(command[4]);
                            }
                        } else if (command[1] == STOP) {
                            Serial.println("    STOP Command");
                            motor->stop();
                        } else if (command[1] == START) {
                            Serial.println("    START Command : ");
                            Serial.print("        dir : ");
                            Serial.println(motor->getDirection());
                            Serial.print("        speed : ");
                            Serial.println(motor->getSpeed());
                            motor->start();
                        } else if (command[1] == SHUTDOWN) {
                            Serial.println("    SHUTDOWN Command");
                            motor->shutdown();
                        }

                    }
                }
                Serial.println("");
            }
        }
        
    
};