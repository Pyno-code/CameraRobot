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
#define LIMITSWITCH_TOP 35
#define LIMITSWITCH_BOTTOM 36

int counter = 0;

OneButton button(BUTTON_PIN, true); // true pour activer le pull-up interne
OneButton limitswitch_top(LIMITSWITCH_TOP, true);
OneButton limitswitch_bottom(LIMITSWITCH_BOTTOM, true);

bool running = false;
int dir = 1;

FastAccelStepperEngine engine = FastAccelStepperEngine();
FastAccelStepper *stepper_mid = NULL;

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

void test1() {
  counter++;
  Serial.print("Test 1 : bottom");
  Serial.println(counter);
}

void test2() {
  counter++;
  Serial.print("Test 2 : top");
  Serial.println(counter);
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

  limitswitch_bottom.attachLongPressStart(test1);
  limitswitch_top.attachLongPressStart(test2);

  
  
  engine.init();

  stepper_mid = engine.stepperConnectToPin(STEP_PIN_MID); // STEP pin connected to STEP_PIN_MID
  stepper_mid->setDirectionPin(DIR_PIN_MID);
  stepper_mid->setSpeedInHz(1000); // Set speed in Hz
  stepper_mid->setAcceleration(10000); // Set acceleration in steps/s^2
  stepper_mid->runForward();
  
}

void loop() {
  button.tick(); // Nécessaire pour vérifier l'état du bouton
  limitswitch_bottom.tick();
  limitswitch_top.tick();

  if (running) {
  }
}
