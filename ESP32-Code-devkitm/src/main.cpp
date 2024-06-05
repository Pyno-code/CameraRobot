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
FastAccelStepper *stepper_base = nullptr;
FastAccelStepper *stepper_mid = nullptr;
FastAccelStepper *stepper_top = nullptr;

void singleClick() {
  running = !running;
  Serial.print("Running state: ");
  Serial.println(running);
  if (running) {
    if (dir == 1) {
      stepper_mid->runForward();
    } else {
      stepper_mid->runBackward();
    }
  } else {
    stepper_mid->stopMove();
  }
  
}

void doubleClick() {
  dir = -dir;
  if (running) {
    stepper_mid->stopMove();
    if (dir == 1) {
      stepper_mid->runForward();
    } else {
      stepper_mid->runBackward();
    }
  }
}

void setup() {
  Serial.begin(115200);

  delay(1000); 
  Serial.println("Starting...");
  button.attachClick(singleClick);
  button.attachDoubleClick(doubleClick);
  
  
  engine.init();
  stepper_base = engine.stepperConnectToPin(STEP_PIN_BASE); // STEP pin connected to STEP_PIN_BASE
  stepper_base->setDirectionPin(DIR_PIN_BASE);
  stepper_base->setSpeedInHz(50); // Set speed in Hz
  stepper_base->setAcceleration(10000); // Set acceleration in steps/s^2

  stepper_mid = engine.stepperConnectToPin(STEP_PIN_MID); // STEP pin connected to STEP_PIN_MID
  stepper_mid->setDirectionPin(DIR_PIN_MID);
  stepper_mid->setSpeedInHz(50); // Set speed in Hz
  stepper_mid->setAcceleration(10000); // Set acceleration in steps/s^2

  stepper_top = engine.stepperConnectToPin(STEP_PIN_TOP); // STEP pin connected to STEP_PIN_TOP
  stepper_top->setDirectionPin(DIR_PIN_TOP);
  stepper_top->setSpeedInHz(50); // Set speed in Hz
  stepper_top->setAcceleration(10000); // Set acceleration in steps/s^2

}

void loop() {
  button.tick(); // Nécessaire pour vérifier l'état du bouton

  if (running) {
  }
}


