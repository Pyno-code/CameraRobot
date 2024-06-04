#include <Arduino.h>
#include <OneButton.h>

#include <Arduino.h>
#include <FastAccelStepper.h>

#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_MID  7
#define DIR_PIN_MID   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4

#define BUTTON_PIN 12

OneButton button(BUTTON_PIN, true); // true pour activer le pull-up interne

bool running = false;
int dir = 1;

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper_base = NULL;

void singleClick() {
  running = !running;
  Serial.print("Running state: ");
  Serial.println(running);
  if (running) {
    if (dir == 1) {
      stepper_base->runForward();
    } else {
      stepper_base->runBackward();
    }
  } else {
    stepper_base->stopMove();
  }
  
  
}

void doubleClick() {
  dir = -dir;
  if (running) {
    stepper_base->stopMove();
    if (dir == 1) {
      stepper_base->runForward();
    } else {
      stepper_base->runBackward();
    }
  }
}


