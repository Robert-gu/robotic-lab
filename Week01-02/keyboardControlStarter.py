# teleoperate the robot through keyboard control
# getting-started code

from pynput.keyboard import Key, Listener, KeyCode
import cv2
import numpy as np

class Keyboard:
    # feel free to change the speed, or add keys to do so
    wheel_vel_forward = 20
    wheel_vel_rotation = 20

    def __init__(self, ppi=None):
        # storage for key presses
        self.directions = [False for _ in range(4)]
        self.signal_stop = False 
        self.speed_up=False

        # connection to PenguinPi robot
        self.ppi = ppi
        self.wheel_vels = [0, 0]

        self.listener = Listener(on_press=self.on_press, on_release=self.on_release).start()

    def on_release(self, key):
        #print(f"released {key}")       
        if key == KeyCode.from_char('w'):
            self.directions[0] = False
        elif key == KeyCode.from_char('s'):
            self.directions[1] = False
        elif key == KeyCode.from_char('a'):
            self.directions[2] = False
        elif key == KeyCode.from_char('d'):
            self.directions[3] = False
        elif key == Key.shift:
            self.speed_up = False

        self.send_drive_signal()

    def on_press(self, key):
        #print(f"pressed {key}")       
        # use arrow keys to drive, space key to stop
        # feel free to add more keys

        if key == KeyCode.from_char('w'):
            self.directions[0] = True
        elif key == KeyCode.from_char('s'):
            self.directions[1] = True
        elif key == KeyCode.from_char('a'):
            self.directions[2] = True
        elif key == KeyCode.from_char('d'):
            self.directions[3] = True
        #elif key == Key.space:
        #   self.signal_stop = True
        elif key == Key.shift:
            self.speed_up = True
        
        self.send_drive_signal()

    def get_drive_signal(self):           
        # translate the key presses into drive signals 
        speed = Keyboard.wheel_vel_forward
        speed_increase = 100
        turning_speed = Keyboard.wheel_vel_rotation

        #move forward 
        left_speed = 0
        right_speed = 0

        if self.speed_up == True:
            speed= Keyboard.wheel_vel_forward+speed_increase;
        else:
            speed= Keyboard.wheel_vel_forward;
        
        if self.directions[0] == True : #forward
            left_speed = speed;
            right_speed = speed;

        elif self.directions[1] == True : #backwards
            left_speed = -speed;
            right_speed = -speed;

        elif self.directions[2] == True: # Left
            left_speed = -turning_speed;
            right_speed = turning_speed;

        elif self.directions[3] ==True: # Right
            left_speed = turning_speed;
            right_speed = -turning_speed;

        #print(self.directions)
        '''elif self.signal_stop == True:
            left_speed = 0
            right_speed = 0

        self.signal_stop = False

        # reset directions array
        for i in range(len(self.directions)):
            self.directions[i] = False;'''

        return left_speed, right_speed

    def send_drive_signal(self):
        if not self.ppi is None:
            lv, rv = self.get_drive_signal()
            lv, rv = self.ppi.set_velocity(lv, rv)
            self.wheel_vels = [lv, rv]

    def latest_drive_signal(self):
        return self.wheel_vels


if __name__ == "__main__":
    import penguinPiC
    ppi = penguinPiC.PenguinPi()

    keyboard_control = Keyboard(ppi)

    cv2.namedWindow('video', cv2.WINDOW_NORMAL);
    cv2.setWindowProperty('video', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE);

    while True:
        # font display options
        font = cv2.FONT_HERSHEY_SIMPLEX
        location = (0, 0)
        font_scale = 1
        font_col = (255, 255, 255)
        line_type = 2

        # get velocity of each wheel
        wheel_vels = keyboard_control.latest_drive_signal();
        L_Wvel = wheel_vels[0]
        R_Wvel = wheel_vels[1]

        # get current camera frame
        curr = ppi.get_image()

        # scale to 144p
        # feel free to change the resolution
        resized = cv2.resize(curr, (960, 720), interpolation = cv2.INTER_AREA)

        # feel free to add more GUI texts
        cv2.putText(resized, f"PenguinPi: velocity (left) {L_Wvel}, (right) {R_Wvel}", (15, 100), font, font_scale, font_col, line_type)
        cv2.putText(resized, f"Controls: WASD to move, hold Shift to speed up", (15, 50), font, font_scale, font_col, line_type)
        cv2.imshow('video', resized)
        cv2.waitKey(1)

        continue
