

#include <FastAccelStepper.h>
inline const char * typeStr (int   var) { return " int "; }
inline const char * typeStr (long  var) { return " long "; }
inline const char * typeStr (float var) { return " float "; }
inline const char * typeStr (const char *var) { return " char "; }


class Motor {

    private:
        int steps_per_revolution = 200;
        int dir = 1;
        FastAccelStepper *stepper;
        int id;
        

    public:
        Motor(FastAccelStepperEngine engine_, int id_, int step_pin, int dir_pin, int steps_per_revolution_) {
            id = id_;

            steps_per_revolution = steps_per_revolution_;
            // Serial.println(steps_per_revolution);
            // Serial.println(typeStr(steps_per_revolution));
            Serial.print("Motor ID: ");
            Serial.println(id);
            FastAccelStepperEngine engine = FastAccelStepperEngine();
            Serial.println("Engine created");
            engine.init();
            Serial.println("Engine initialized");
            stepper = engine_.stepperConnectToPin(step_pin);
            Serial.println("Stepper connected to pin");
            stepper->setDirectionPin(dir_pin);
            stepper->setSpeedInHz(100);
            stepper->setAcceleration(2500);
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
            // stepper->setSpeedInHz((speed < 0 ? -speed : speed));
            stepper->setSpeedInHz(speed);
            Serial.print("Speed set to: ");
            Serial.println(stepper->getSpeedInMilliHz() / 1000);
            Serial.print("Setting dir to: ");
            Serial.println(dir);
        }

        void moveAngle(float angle) {
            float step_ = angle * steps_per_revolution / 360 ;
            int step = (int) step_;
            stepper->move(step);
        }

        void moveTo(int position) {
            stepper->moveTo(position);
        }

        // void moveToAngle(float angle) {
        //     stepper->moveTo(int(angle * steps_per_revolution / 360));
        // }

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
            if (dir >= 0) {
                Serial.println("Running forward");
                runForward();
            } else {
                Serial.println("Running backward");
                runBackward();
            }
            
        }

        int getDirection() {
            return dir;
        }

        float getSpeed() {
            return stepper->getSpeedInMilliHz() / 1000;
        }

        int getStepsPerRevolution() {
            return steps_per_revolution;
        }

        int getID() {
            return id;
        }

};