#include <AccelStepper.h>

class Moteur {
private:
    int stepPin;
    int dirPin;
    long target_step_position = 0;
    long target_angle_position = 0;
    float microstepping = 0;
    int speed = 0;

    AccelStepper stepper;

public:
    Moteur(int stepPin, int dirPin, int speed, float microstepping) : microstepping(microstepping), stepPin(stepPin), dirPin(dirPin), speed(speed), stepper(AccelStepper::DRIVER, stepPin, dirPin) {
        resetSpeed();
        stepper.setAcceleration(speed/2);
    }
    
    void setSpeed(int speed_) {
        speed = speed_;
        stepper.setSpeed(speed);
    }

    void resetSpeed() {
        stepper.setSpeed(speed);
    }

    void setTargetPosition(int position) {
        target_step_position = position;
        target_angle_position = position*microstepping;
    }

    void setTargetRelativePosition(int relative_position) {
        target_step_position += relative_position;
        target_angle_position += relative_position*microstepping;
    }

    void setTargetAngle(long angle) {
        target_angle_position = angle;
        target_step_position = int(target_angle_position/microstepping);
    }
    
    void setTargetRelativeAngle(long angle) {
        target_angle_position += angle;
        target_step_position = int(target_angle_position/microstepping);
    }

    long getCurrentPosition() {
        return stepper.currentPosition();
    }

    long getCurrentAngle() {
        return stepper.currentPosition()*microstepping;
    }

    long getTargetPosition() {
        return target_step_position;
    }

    long getTargetAngle() {
        return target_angle_position;
    }

    void move(){
        resetSpeed();
        stepper.run();
    }

    void moveToPosition() {
        // check if it does it in the two direction
        if ((stepper.currentPosition() != target_step_position))
            resetSpeed();
            stepper.run();
    }

    void setCurrentPosition(int position) {
        stepper.setCurrentPosition(position);
    }

    void setCurrentAngle(long angle) {
        stepper.setCurrentPosition(angle/microstepping);
    }
};
#define STEP_PIN_BASE   10
#define DIR_PIN_BASE   9

#define STEP_PIN_BOTTOM  7
#define DIR_PIN_BOTTOM   6

#define STEP_PIN_TOP  5
#define DIR_PIN_TOP   4

class ControlMotors {
    private:
        Moteur stepper_base;
        Moteur stepper_bottom;
        Moteur stepper_top;
    
    public:
        ControlMotors() : 
            stepper_base(Moteur(STEP_PIN_BASE, DIR_PIN_BASE, 1, 1.8)),
            stepper_bottom(Moteur(STEP_PIN_BOTTOM, DIR_PIN_BOTTOM, 1, 1.8)),
            stepper_top(Moteur(STEP_PIN_TOP, DIR_PIN_TOP, 1/4, 1.8/4)) {
            moveMotors(360, 360, 360);
        }

        void moveMotors(long angle_top, long angle_bottom, long angle_base) {
            stepper_top.setTargetAngle(angle_top);
            stepper_bottom.setTargetAngle(angle_bottom);
            stepper_base.setTargetAngle(angle_base);
        }

        void loop() {
            stepper_base.moveToPosition();
            stepper_bottom.moveToPosition();
            stepper_top.moveToPosition();

            if (stepper_top.getCurrentPosition() == stepper_top.getTargetPosition()) {
                moveMotors(-stepper_top.getCurrentPosition(), -stepper_bottom.getCurrentPosition(), -stepper_base.getCurrentPosition());
            }
        }

};