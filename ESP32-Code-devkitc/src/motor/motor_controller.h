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
        FastAccelStepperEngine engine = FastAccelStepperEngine();
        Motor* stepper_base;
        Motor* stepper_middle;
        Motor* stepper_top;
        std::vector<std::array<float, 10>>* commandQueue;
        std::map<int, Motor*> motors = {};
        
    public:
        MotorController(std::vector<std::array<float, 10>> *commandQueue_) {
            engine.init();
            commandQueue = commandQueue_;
            stepper_base = new Motor(engine, STEP_PIN_BASE, DIR_PIN_BASE, 200);
            stepper_middle = new Motor(engine, STEP_PIN_MID, DIR_PIN_MID, 200);
            stepper_top = new Motor(engine, STEP_PIN_TOP, DIR_PIN_TOP, 800);

            motors[MOTOR_BASE] = stepper_base;
            motors[MOTOR_MIDDLE] = stepper_middle;
            motors[MOTOR_TOP] = stepper_top;
        }

        void loop() {
            if (commandQueue->size() > 0) {
                std::array<float, 10> command = (*commandQueue)[0];
                commandQueue->erase(commandQueue->begin());
                logger::print(logger::INFO, "Command received: ");
                int motor_id = static_cast<int>(command[3]);
                logger::print(logger::INFO, "Motor id: ", false);
                Serial.println(motor_id);

                if (motor_id == ALL) {
                    // do nothing for now
                } else if (command[0] == MOTOR) {
                    if (command[1] == SET) {
                        logger::print(logger::INFO, "SET : ");
                        if (command[2] == ANGLE) {
                            int motor_id = static_cast<int>(motor_id);
                            Motor* motor = motors[motor_id];
                            logger::print(logger::INFO, "Moving motor to angle: ", false);
                            Serial.println(command[4]);
                            motor->moveAngle(command[4]);
                        } else if (command[2] == SPEED) {
                            Motor* motor = motors[(motor_id)];
                            logger::print(logger::INFO, "Setting speed to: ", false);
                            Serial.println(command[4]);
                            motor->setSpeed(command[4]);
                            logger::print(logger::INFO, "Dir : ", false);
                            Serial.println(motor->getDirection());
                        }
                    } else if (command[1] == STOP) {
                        Motor* motor = motors[(motor_id)];
                        motor->stop();
                        logger::print(logger::INFO, "Stopping motor");
                    } else if (command[1] == START) {
                        Motor* motor = motors[(motor_id)];
                        logger::print(logger::INFO, "Starting motor");
                        logger::print(logger::INFO, "Dir : ", false);
                        Serial.println(motor->getDirection());
                        motor->start();

                    } else if (command[1] == SHUTDOWN) {
                        Motor* motor = motors[(motor_id)];
                        logger::print(logger::INFO, "Shutting down motor");
                        motor->shutdown();
                    }
                }
            }
        }
        
    
};