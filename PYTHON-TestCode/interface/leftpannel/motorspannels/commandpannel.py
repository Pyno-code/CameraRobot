import tkinter as tk

from interface.utils.toggleswitch import ToggleSwitch

class MotorsCommandPannel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg="white")  # Just to differentiate visually

        # Add widgets for command panel
        command_label = tk.Label(self, text="Command Panel (Motors)")
        command_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        arm_motor_label = tk.Label(self, text="Arm Motor")
        arm_motor_label.grid(row=1, column=0, columnspan=2, pady=20)
        
        label_speed_arm_motor = tk.Label(self, text="Speed % :")
        label_speed_arm_motor.grid(row=2, column=0, pady=3)

        self.slider_speed_arm_motor = tk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, resolution=1)
        self.slider_speed_arm_motor.grid(row=2, column=1, columnspan=2, sticky='ew')
        self.slider_speed_arm_motor.bind("<ButtonRelease>", self.on_speed_change_arm_motor)

        self.start_button_arm_motor = ToggleSwitch(self, func=self.trigger_arm_motor)
        self.start_button_arm_motor.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.start_button_arm_motor.configure(text="Arm motor activation")




        hand_motor_label = tk.Label(self, text="Hand Motor")
        hand_motor_label.grid(row=4, column=0, columnspan=2, pady=20)
        
        label_speed_hand_motor = tk.Label(self, text="Speed % :")
        label_speed_hand_motor.grid(row=5, column=0, pady=3)

        self.slider_speed_hand_motor = tk.Scale(self, from_=-100, to=100, orient=tk.HORIZONTAL, resolution=1)
        self.slider_speed_hand_motor.grid(row=5, column=1, columnspan=2, sticky='ew')
        self.slider_speed_hand_motor.bind("<ButtonRelease>", self.on_speed_change_hand_motor)

        self.start_button_hand_motor = ToggleSwitch(self, func=self.trigger_hand_motor)
        self.start_button_hand_motor.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.start_button_hand_motor.configure(text="Hand motor activation")

        

        self.shutdown_button = tk.Button(self, text="Shutdown", bg="magenta", fg="white")
        self.shutdown_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.shutdown_button.bind("<Button-1>", self.shutdown)

        self.label_key_handler = tk.Label(self, text="Key Handler :")
        self.label_key_handler.grid(row=8, column=0, pady=3)
        self.key_handler_button = ToggleSwitch(self, func=self.key_handler)
        self.key_handler_button.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

        # Add more widgets as needed
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def on_speed_change_hand_motor(self, event):
        print(f"Speed changed to {self.slider_speed_hand_motor.get()}")

    def on_speed_change_arm_motor(self, event):
        print(f"Speed changed to {self.slider_speed_arm_motor.get()}")

    def trigger_hand_motor(self):
        if not self.key_handler_button.get_state():
            if self.start_button_hand_motor.get_state():
                print("Hand motor started")
            else:
                print("Hand motor stopped")
    
    def trigger_arm_motor(self):
        if not self.key_handler_button.get_state():
            if self.start_button_arm_motor.get_state():
                print("Arm motor started")
            else:
                print("Arm motor stopped")
    
    def shutdown(self, event):
        print("Shutdown button clicked")


    def key_handler(self):
        if self.key_handler_button.get_state():
            print("Key handler activated")
            self.start_button_arm_motor.set_state(False)
            self.start_button_hand_motor.set_state(False)
        else:
            print("Key handler deactivated")
    