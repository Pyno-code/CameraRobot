

#include <FastAccelStepper.h>


class Motor {

    private:
        FastAccelStepperEngine engine;
        FastAccelStepper *stepper;
        int steps_per_revolution;
        int dir = 1;

    public:
        Motor(FastAccelStepperEngine engine_, int step_pin, int dir_pin, int steps_per_revolution_) {
            steps_per_revolution = steps_per_revolution_;            
            engine = engine_;
            engine.init();
            stepper = engine.stepperConnectToPin(step_pin);
            stepper->setDirectionPin(dir_pin);
            stepper->setSpeedInHz(100);
            stepper->setAcceleration(100);
        }
    
        void move(int position) {
            stepper->move(position);
        }

        void setSpeed(float speed) {
            if (speed < 0) {
                dir = -1;
            } else {
                dir = 1;
            }

            stepper->setSpeedInHz((speed < 0 ? -speed : speed));
        }

        void moveAngle(float angle) {
            int step = int(angle * steps_per_revolution / 360);
            stepper->move(step);
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

        void stop() {
            stepper->stopMove();
        }

        void shutdown() {
            stepper->forceStop();
        }

        void start() {
            if (dir > 0) {
                runForward();
            } else {
                runBackward();
            }
            
        }

        int getDirection() {
            return dir;
        }

};