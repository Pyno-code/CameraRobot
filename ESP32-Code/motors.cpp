

#include <AccelStepper.h>

#define STEP_PIN  11
#define DIR_PIN   10

AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);


void setup() {
  stepper.setMaxSpeed(1000);   // Vitesse maximale du moteur (en pas par seconde)
  stepper.setAcceleration(500); // Accélération du moteur (en pas par seconde par seconde)

  // Vous pouvez également inverser la direction du moteur si nécessaire
  // stepper.setPinsInverted(false, true, false); // Inverse la direction
}


void loop() {
  // Fait avancer le moteur de 2000 pas
  stepper.moveTo(2000);
  stepper.runToPosition();

  // Attend un peu
  delay(1000);

  // Fait reculer le moteur de 2000 pas
  stepper.moveTo(0);
  stepper.runToPosition();

  // Attend un peu
  delay(1000);
}
