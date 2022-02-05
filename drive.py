#!/usr/bin/env python

from pickle import FALSE
from random import randrange
import time
from lib.motor import Motor
from lib.servo import Servo
from lib.ultrasonic import Ultrasonic 
from lib.pwm import PWM
from lib.pin import Pin

fwd_speed = 30
bwd_speed = 15
turn_speed = 10
ultrasonic_servo_offset = 0 

ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

# Init Ultrasonic
us = Ultrasonic(Pin('D8'), Pin('D9'))

# Init Servo
servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

# Init motors
left_front = Motor(PWM("P13"), Pin("D4"), is_reversed=False) # motor 1
right_front = Motor(PWM("P12"), Pin("D5"), is_reversed=False) # motor 2
left_rear = Motor(PWM("P8"), Pin("D11"), is_reversed=False) # motor 3
right_rear = Motor(PWM("P9"), Pin("D15"), is_reversed=False) # motor 4

def get_distance_at(angle):
    global angle_distance
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    angle_distance = [angle, distance]
    return distance

def get_status_at(angle, ref1=35, ref2=10):
    dist = get_distance_at(angle)
    if dist > ref1 or dist == -2:
        return 2
    elif dist > ref2:
        return 1
    else:
        return 0

def scan_step(ref):
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    status = get_status_at(current_angle, ref1=ref)#ref1

    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

########################################################
# Motors
def forward(power):
    left_front.set_power(power)
    left_rear.set_power(power)
    right_front.set_power(power)
    right_rear.set_power(power)

def backward(power):
    left_front.set_power(-power)
    left_rear.set_power(-power)
    right_front.set_power(-power)
    right_rear.set_power(-power)

def turn_left(power):
    left_front.set_power(-power)
    left_rear.set_power(-power)
    right_front.set_power(power)
    right_rear.set_power(power)

def turn_right(power):
    left_front.set_power(power)
    left_rear.set_power(power)
    right_front.set_power(-power)
    right_rear.set_power(-power)

def stop():
    left_front.set_power(0)
    left_rear.set_power(0)
    right_front.set_power(0)
    right_rear.set_power(0)

def set_motor_power(motor, power):
    if motor == 1:
        left_front.set_power(power)
    elif motor == 2:
        right_front.set_power(power)
    elif motor == 3:
        left_rear.set_power(power)
    elif motor == 4:
        right_rear.set_power(power)

def main():
    while True:
        scan_list = scan_step(35)
        if not scan_list:
            continue
        print("scan_list : " ,scan_list)
        tmp = scan_list[3:7]
        print("tmp : ",tmp)
        if tmp != [2,2,2,2]:
            stop()
            direction = randrange(1,3)
            turn_speed = randrange(10,31)
            backward(bwd_speed)
            time.sleep(0.1)
            if direction == 1:
                turn_left(turn_speed)
            else:    
                turn_right(turn_speed)
            time.sleep(0.1)
        else:
            forward(fwd_speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        stop()
