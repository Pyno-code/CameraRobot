#include <Arduino.h>
#include <AccelStepper.h>
#include <motors/motors_controller.h>


#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_BOTTOM  16
#define DIR_PIN_BOTTOM   15

#define STEP_PIN_TOP  7
#define DIR_PIN_TOP   6

#define PIN_BUTTON 12

int buttonState;            // the current reading from the input pin
int lastButtonState = LOW;  // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

// ControlMotors motor_controler;


bool running = false;
// int i = 0;

void setup() {
  // motor_controler = ControlMotors();
  Serial.begin(115200);

  Serial.println("Starting...");
  pinMode(PIN_BUTTON, INPUT_PULLUP);

  Serial.println("Started");
}


void loop() {

  int reading = digitalRead(PIN_BUTTON);

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
    Serial.println("Running");
    // motor_controler.loop();
  }

  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;
}


