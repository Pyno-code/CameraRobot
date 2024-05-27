#include <AccelStepper.h>

class Motor : public AccelStepper {
    private:
        float microSteping;
    public:
        Motor(uint8_t stepPin, uint8_t dirPin, float microStepping_) : AccelStepper(AccelStepper::DRIVER, stepPin, dirPin) {
            microSteping = microStepping_;
        }

        void init() {
            setMaxSpeed(200*20);
            setSpeed(200*20);
            setAcceleration(200*20);
        }

        void setSpeed(float speed) {
            AccelStepper::setSpeed(speed * microSteping/200);
            Serial.print("Speed: ");
            Serial.println(speed);
        }

        void setMaxSpeed(float speed) {
            AccelStepper::setMaxSpeed(speed * microSteping/200);
        }

        void setTargetPosition(long position) {
            AccelStepper::moveTo(position * microSteping/200);
            setSpeed(200);
        }

        void addTargetPosition(long position) {
            AccelStepper::move(position * microSteping/200);
            setSpeed(200);
        }

        void setTargetAngle(float angle) {
            setTargetPosition(angle * microSteping/1.8);
        }

        void addTargetAngle(float angle) {
            addTargetPosition(angle * microSteping/1.8);
        }

        void changeDirection() {
            setSpeed(-speed());
        }

        void setPositiveDirection() {
            setSpeed(abs(speed()));
        }

        void setNegativeDirection() {
            setSpeed(-abs(speed()));
        }





};

#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_BOTTOM  7
#define DIR_PIN_BOTTOM   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4
