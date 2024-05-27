#include <Arduino.h>
#include <OneButton.h>

#include <Arduino.h>
#include <AccelStepper.h>
#include <motors/motors_controller.h>

#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_MID  7
#define DIR_PIN_MID   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4

#define BUTTON_PIN 12

OneButton button(BUTTON_PIN, true); // true pour activer le pull-up interne

bool running = false;
bool changeDirection = false;

AccelStepper stepper_base(AccelStepper::DRIVER, STEP_PIN_BASE, DIR_PIN_BASE);

void singleClick() {
  running = !running;
  Serial.print("Running state: ");
  Serial.println(running);
}

void doubleClick() {
  changeDirection = true;
}

void setup() {
  Serial.begin(115200);

  delay(1000); 
  Serial.println("Starting...");
  button.attachClick(singleClick);
  button.attachDoubleClick(doubleClick);

  stepper_base.setMaxSpeed(10000);
  stepper_base.setSpeed(100);

  stepper_base.moveTo(100);
  stepper_base.setAcceleration(1000);
}

void loop() {
  button.tick(); // Nécessaire pour vérifier l'état du bouton

  if (running) {
    stepper_base.runSpeedToPosition();
  }
  if (changeDirection) {
    Serial.println("Changing direction");
    
    changeDirection = false;
    stepper_base.setSpeed(-stepper_base.speed());
    if (stepper_base.speed() > 0) {
      Serial.println("Sens trigo axe");
    } else {
      Serial.println("Sens anti-trigo axe");
    }
  }
}


