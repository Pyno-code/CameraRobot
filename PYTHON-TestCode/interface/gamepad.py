from inputs import get_gamepad
import inputs


JOY_LEFT_X = 'ABS_X'
JOY_LEFT_Y = 'ABS_Y'
TRIG_LEFT_Z = 'ABS_Z'

JOY_RIGHT_X = 'ABS_RX'
JOY_RIGHT_Y = 'ABS_RY'
TRIG_RIGHT_Z = 'ABS_RZ'


class Gamepad:

    def __init__(self) -> None:
        self.trigger_dict  = {
            JOY_LEFT_X : 0,
            JOY_LEFT_Y : 0,

            "TRIG_Z" : 0,

            JOY_RIGHT_X : 0,
            JOY_RIGHT_Y : 0,
        }

        self.updated = False

    def loop(self):
        try:
            events = get_gamepad()
            dict_temp = self.trigger_dict.copy()

            for event in events:
                print(event.ev_type, event.code, event.state)
                if event.ev_type == 'Key':
                    pass
                    # print(f'Bouton {event.code} {"pressé" if event.state else "relâché"}')
                elif event.ev_type == 'Absolute':
                    if event.code in [TRIG_LEFT_Z, TRIG_RIGHT_Z]:
                        if event.code == TRIG_RIGHT_Z:
                            dir = 0
                            if event.state > 10:
                                dir = 1
                            else:
                                dir = 0
                        if event.code == TRIG_LEFT_Z:
                            dir = 0
                            if event.state > 10:
                                dir = -1
                            else:
                                dir = 0
                        self.trigger_dict["TRIG_Z"] = dir
                        # print(f'Trigger TRIG_Z : {self.trigger_dict["TRIG_Z"]}')

                    elif event.code in [JOY_LEFT_X, JOY_LEFT_Y, JOY_RIGHT_X, JOY_RIGHT_Y]:
                        dir = 0
                        if event.state > 1000:
                            dir = 1
                        elif event.state < -1000:
                            dir = -1
                        else:
                            dir = 0
                        self.trigger_dict[event.code] = dir
                        
                        # print(f'Joystick {event.code} : {dir}')
                        # print(event.state)
                
            self.updated =  dict_temp != self.trigger_dict
        except inputs.UnpluggedError:
            print("Manette débranchée")
            pass



if __name__ == '__main__':
    gamepad = Gamepad()
    while True:
        gamepad.loop()