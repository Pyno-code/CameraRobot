#include <Arduino.h>
#include <AccelStepper.h>
#include <motors/motors_controller.h>

#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_BOTTOM  7
#define DIR_PIN_BOTTOM   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4

#define PIN_BUTTON 12

// Variables will change:
int ledState = HIGH;        // the current state of the output pin
int buttonState;            // the current reading from the input pin
int lastButtonState = LOW;  // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers


// Moteur stepper_base(STEP_PIN_BASE, DIR_PIN_BASE, 1.8);
// Moteur stepper_bottom(STEP_PIN_BOTTOM, DIR_PIN_BOTTOM, 1.8);
// Moteur stepper_top(STEP_PIN_TOP, DIR_PIN_TOP, 1.8/4);

AccelStepper stepper_base(AccelStepper::DRIVER, STEP_PIN_BASE, DIR_PIN_BASE);
AccelStepper stepper_bottom(AccelStepper::DRIVER, STEP_PIN_BOTTOM, DIR_PIN_BOTTOM);
AccelStepper stepper_top(AccelStepper::DRIVER, STEP_PIN_TOP, DIR_PIN_TOP);




bool running = false;
// int i = 0;

void setup() {
  Serial.begin(115200);

  Serial.println("Starting...");
  pinMode(PIN_BUTTON, INPUT_PULLUP);


  stepper_base.setMaxSpeed(100);
  stepper_base.setSpeed(-100);

  Serial.println("Started");
}


void loop() {

  // stepper_base.move();
  // stepper_bottom.move();
  // stepper_top.move();

  // // stepper_bottom.moveTo(200);
  // // stepper_top.moveTo(800);

  // // stepper_bottom.runToPosition();
  // // stepper_top.runToPosition();

  // read the state of the switch into a local variable:
  int reading = digitalRead(PIN_BUTTON);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == LOW) {
        running = !running;
        Serial.print("Running state: ");
        Serial.println(running);
      } 
    }
  }

  if (running) {
      stepper_base.runSpeed();
  }

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;
}


