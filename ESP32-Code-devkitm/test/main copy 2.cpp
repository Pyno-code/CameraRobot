#include <Arduino.h>
#include <OneButton.h>

#include <Arduino.h>
#include <FastAccelStepper.h>
#include <motor/motor.h>

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
Motor *motor_base;


void singleClick() {
  if (!stepper_base->isRunning()) {
    if (stepper_base->getCurrentPosition() == 5000) {
      stepper_base->moveTo(0);
    } else {
      stepper_base->moveTo(5000);
    }
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

void setup() {
  Serial.begin(115200);

  delay(1000); 
  // Serial.println("Starting...");
  // button.attachClick(singleClick);
  // button.attachDoubleClick(doubleClick);
  
  
  engine.init();
  motor_base = new Motor(engine, STEP_PIN_BASE, DIR_PIN_BASE, 200);
}

void loop() {
  button.tick(); // Nécessaire pour vérifier l'état du bouton

  if (running) {
  }
}


