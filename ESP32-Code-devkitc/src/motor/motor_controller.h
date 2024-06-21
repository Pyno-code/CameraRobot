#include <FastAccelStepper.h>
#include <logger.h>
#include <map>
#include <string>
#include <iostream>
#include <vector>
#include <button/limit_switch.h>


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
#define INITIALIZATION  4

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

#define BUTTON_PIN 12
#define PIN_LIMITSWITCH_TOP 35
#define PIN_LIMITSWITCH_MIDDLE 36

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
        FastAccelStepper* stepper_base;
        int dir_base = 1;
        int base_step_per_rev = 200;

        FastAccelStepper* stepper_middle;
        int dir_middle = 1;
        int middle_step_per_rev = 200;

        FastAccelStepper* stepper_top;
        int dir_top = 1;
        int top_step_per_rev = 800;

        std::vector<std::array<float, 10>>* commandQueue;
        bool initialization = false;
        int phase = 0;

        LimitSwitch limitSwitchTop = LimitSwitch(PIN_LIMITSWITCH_TOP, 10);
        LimitSwitch limitSwitchMiddle = LimitSwitch(PIN_LIMITSWITCH_MIDDLE, 10);
        LimitSwitch limitSwitchTest = LimitSwitch(BUTTON_PIN, 10);
        
    public:
        MotorController(std::vector<std::array<float, 10>> *commandQueue_) {
            engine.init();
            commandQueue = commandQueue_;

            stepper_base = engine.stepperConnectToPin(STEP_PIN_BASE);
            stepper_base->setDirectionPin(DIR_PIN_BASE);
            stepper_base->setSpeedInHz(50); // Set speed in Hz
            stepper_base->setAcceleration(5000); // Set acceleration in steps/s^2

            stepper_middle = engine.stepperConnectToPin(STEP_PIN_MID); // STEP pin connected to STEP_PIN_MID
            stepper_middle->setDirectionPin(DIR_PIN_MID);
            stepper_middle->setSpeedInHz(50); // Set speed in Hz
            stepper_middle->setAcceleration(5000); // Set acceleration in steps/s^2

            stepper_top = engine.stepperConnectToPin(STEP_PIN_TOP); // STEP pin connected to STEP_PIN_TOP
            stepper_top->setDirectionPin(DIR_PIN_TOP);
            stepper_top->setSpeedInHz(50); // Set speed in Hz
            stepper_top->setAcceleration(80000); // Set acceleration in steps/s^2

        }

        void loop() {


            limitSwitchTest.update();

            // Serial.println("Looping");
            // Serial.print("Limit Switch Test : ");
            // Serial.println(limitSwitchTest.isPressed());
            // Serial.print("Initialization : ");
            // Serial.println(initialization);



            if (limitSwitchTest.isPressed() || initialization) {
                // } else if (command[0] == INITIALIZATION) || initialization {
                Serial.println("INITIALIZATION Command");
                limitSwitchMiddle.update();
                limitSwitchTop.update();
                if (!initialization) {
                    Serial.println("initialization false, switching");
                    initialization = true;
                    phase = 0;
                    stepper_top->setSpeedInHz(200);
                    stepper_top->stopMove();
                    stepper_middle->setSpeedInHz(50);
                    stepper_middle->stopMove();
                    stepper_middle->runForward();
                }
                if (phase == 0) {
                    Serial.println("Phase 0");
                    stepper_middle->runForward();
                    if (!stepper_middle->isRunning()) {
                        stepper_middle->runForward();
                    }
                    if (limitSwitchMiddle.isPressed()) {
                        stepper_middle->stopMove();
                        phase = 1;
                        Serial.println("passage à la phase 1");
                    }
                } else if (phase == 1) {
                    Serial.println("Phase 1");
                    if (!stepper_middle->isRunning()) {
                        stepper_middle->setSpeedInHz(25);
                        stepper_middle->runBackward();
                    }
                    if (limitSwitchMiddle.isReleased()) {
                        stepper_middle->stopMove();
                        phase = 2;
                    }

                    
                } else if (phase == 2) {
                    Serial.println("Phase 2");
                    if (!stepper_middle->isRunning()) {
                        stepper_middle->runForward();
                    }
                    if (limitSwitchMiddle.isPressed()) {
                        stepper_middle->stopMove();
                        phase = 3;
                        stepper_middle->setCurrentPosition(590);
                        stepper_middle->setSpeedInHz(160);
                        stepper_middle->moveTo(0, true);
                        stepper_middle->setSpeedInHz(0);
                    }
                } else if (phase == 3) {
                    Serial.println("Phase 3");
                    stepper_top->runForward();
                    if (!stepper_top->isRunning()) {
                        stepper_top->runForward();
                    }
                    if (limitSwitchTop.isPressed()) {
                        stepper_top->stopMove();
                        phase = 4;
                        Serial.println("passage à la phase 4");
                    }
                } else if (phase == 4) {
                    Serial.println("Phase 4");
                    if (!stepper_top->isRunning()) {
                        stepper_top->setSpeedInHz(100);
                        stepper_top->runBackward();
                    }
                    if (limitSwitchTop.isReleased()) {
                        stepper_top->stopMove();
                        
                        phase = 5;
                    }

                    
                } else if (phase == 5) {
                    Serial.println("Phase 5");
                    if (!stepper_top->isRunning()) {
                        stepper_top->runForward();
                    }
                    if (limitSwitchTop.isPressed()) {
                        stepper_top->stopMove();
                        stepper_top->setCurrentPosition(20400);
                        stepper_top->setSpeedInHz(1600);
                        stepper_top->moveTo(0, true);
                        initialization = false;
                        stepper_top->setSpeedInHz(0);
                        phase = 0;
                    }
                }
                    
            }


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
                    int motor_id = (int)(command[3]);
                    FastAccelStepper* stepper;
                    int step_per_rev = 0;
                    int* dir = nullptr;

                    if (motor_id != ALL and motor_id != STATUS) {
                        if (motor_id == MOTOR_BASE) {
                            Serial.print("  MOTOR_BASE");
                            stepper = stepper_base;
                            step_per_rev = base_step_per_rev;
                            dir = &dir_base;  // Correctly assign the pointer
                        } else if (motor_id == MOTOR_MIDDLE) {
                            Serial.print("  MOTOR_MIDDLE");
                            stepper = stepper_middle;
                            step_per_rev = middle_step_per_rev;
                            dir = &dir_middle;  // Correctly assign the pointer
                        } else if (motor_id == MOTOR_TOP) {
                            Serial.print("  MOTOR_TOP");
                            stepper = stepper_top;
                            step_per_rev = top_step_per_rev;
                            dir = &dir_top;  // Correctly assign the pointer
                        }
                        Serial.println();

                        if (command[1] == SET) {
                            Serial.println("    SET Command : ");
                            if (command[2] == ANGLE) {
                                Serial.print("      ANGLE Command : ");
                                int angle = (int)command[4] * step_per_rev / 360;
                                stepper->move(angle);
                            } else if (command[2] == SPEED) {
                                Serial.print("      SPEED Command : ");
                                Serial.println("test");
                                Serial.println(dir_base);
                                Serial.println(dir_middle);
                                Serial.println(dir_top);
                                Serial.println("test");

                                if (command[4] > 0) {
                                    *dir = 1;
                                } else {
                                    *dir = -1;
                                }
                                Serial.print("          ");
                                Serial.print("Dir set to : ");
                                Serial.println(*dir);

                                Serial.println(dir_base);
                                Serial.println(dir_middle);
                                Serial.println(dir_top);

                                Serial.println("test");

                                stepper->setSpeedInHz(command[4]);
                                Serial.print("          ");
                                Serial.print("Speed set to : ");
                                Serial.println(stepper->getSpeedInMilliHz() / 1000);
                            }
                        } else if (command[1] == STOP) {
                            Serial.println("    STOP Command");
                            stepper->stopMove();
                        } else if (command[1] == START) {
                            Serial.println("    START Command");
                            Serial.print("      ");
                            Serial.print("Dir set to : ");
                            Serial.println(command[4]);
                            if (command[4] != 0) {*dir = (int) command[4];}
                            if (*dir == 1) {
                                Serial.print("      ");
                                Serial.println("Forward");
                                
                                if (motor_id == MOTOR_TOP) {
                                    if (!(stepper_top->getCurrentPosition() > 20005)) {
                                        stepper->runForward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(20005);
                                    }
                                } else if (motor_id == MOTOR_MIDDLE){
                                    if (!(stepper_middle->getCurrentPosition() > 500)) {
                                        stepper->runForward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(500);
                                    }
                                } else if (motor_id == MOTOR_BASE){
                                    if (!(stepper_base->getCurrentPosition() > 1995)) {
                                        stepper->runForward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(1995);
                                    }
                                }
                                

                            } else {

                                if (motor_id == MOTOR_TOP) {
                                    if (!(stepper_top->getCurrentPosition() < -20005)) {
                                        stepper->runBackward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(-20005);
                                    }
                                } else if (motor_id == MOTOR_MIDDLE){
                                    if (!(stepper_middle->getCurrentPosition() < -1939)) {
                                        stepper->runBackward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(-1939);
                                    }

                                } else if (motor_id == MOTOR_BASE){
                                    if (!(stepper_base->getCurrentPosition() < -1995)) {
                                        stepper->runBackward();
                                    } else {
                                        stepper->stopMove();
                                        stepper->moveTo(-1995);
                                    }
                                }

                                Serial.print("      ");
                                Serial.println("Backward");
                                stepper->runBackward();
                            }
                        } else if (command[1] == SHUTDOWN) {
                            Serial.println("    SHUTDOWN Command");
                            stepper->forceStop();
                        }
                    }
                } else if (limitSwitchTest.isPressed() || initialization) {
                // } else if (command[0] == INITIALIZATION) || initialization {
                    Serial.println("INITIALIZATION Command");
                    limitSwitchMiddle.update();
                    limitSwitchTop.update();
                    if (!initialization) {
                        initialization = true;
                        phase = 0;
                        stepper_top->setSpeedInHz(1600);
                        stepper_top->stopMove();
                        stepper_middle->setSpeedInHz(200);
                        stepper_middle->stopMove();
                    }
                    if (phase == 0) {
                        if (!stepper_top->isRunning()) {
                            stepper_top->runForward();
                        }
                        if (limitSwitchTop.isPressed()) {
                            stepper_top->stopMove();
                            phase = 1;
                        }
                    } else if (phase == 1) {
                        if (!stepper_top->isRunning()) {
                            stepper_top->setSpeedInHz(400);
                            stepper_top->runBackward();
                        }
                        if (limitSwitchTop.isReleased()) {
                            stepper_top->stopMove();

                            phase = 2;
                        }

                        
                    } else if (phase == 2) {
                        if (!stepper_top->isRunning()) {
                            stepper_middle->runForward();
                        }
                        if (limitSwitchMiddle.isPressed()) {
                            stepper_middle->stopMove();
                            phase = 3;
                            stepper_middle->setCurrentPosition(45);
                        }
                    }
                    
                }
                Serial.println("");
            }
        }

        void stopMotor() {
            stepper_base->stopMove();
            stepper_middle->stopMove();
            stepper_top->stopMove();
        }

                
    
};