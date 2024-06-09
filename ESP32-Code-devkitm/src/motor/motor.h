

#include <FastAccelStepper.h>

    
class Motor {

    private:
        FastAccelStepperEngine engine;
        FastAccelStepper *stepper;
        int steps_per_revolution;

    public:
        Motor(FastAccelStepperEngine engine_, int step_pin, int dir_pin, int steps_per_revolution_) {
            steps_per_revolution = steps_per_revolution_;            
            engine = engine_;

            stepper = engine.stepperConnectToPin(step_pin);
            stepper->setDirectionPin(dir_pin);
            stepper->setSpeedInHz(1000);
            stepper->setAcceleration(10000);
            moveTo(5000);
            delay(1000);
            move(5000);
            delay(1000);
            move(360);
            delay(3);
            moveTo(360);


        }
    
        void move(int position) {
            stepper->move(position);
        }

        void moveAngle(float angle) {
            stepper->move(int(angle * steps_per_revolution / 360));
        }

        void moveTo(int position) {
            stepper->moveTo(position);
        }

        void moveToAngle(float angle) {
            stepper->moveTo(int(angle * steps_per_revolution / 360));
        }

        void runForward() {
            stepper->runForward();
        }

        void runBackward() {
            stepper->runBackward();
        }

        void stopMove() {
            stepper->stopMove();
        }
};