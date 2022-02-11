import time
from time import sleep
import numpy as np
import os
import math
from lib.motor import Motor
from lib.servo import Servo
from lib.ultrasonic import Ultrasonic
from lib.pwm import PWM
from lib.pin import Pin

ultrasonic_servo_offset = 0

# Init Ultrasonic
us = Ultrasonic(Pin('D8'), Pin('D9'))

# Init Servo
pan_servo = Servo(PWM("P0"), offset=ultrasonic_servo_offset)

#numpy arrays
gridMap = np.zeros((10,2)) # hold values used to calculate points [x,y]
gridFinal = np.zeros((10,10)) # holds 10 X 10 coordinate map

x_carD = 0 #car distance x value
y_carD = 0 #car distance y value

def get_scan(angle):
    #replaces empty numpy array with [degree of angle, distance from sensor]
    actualAngle = 90
    for i in range(len(gridMap)):
        distance = us.get_distance()
        gridMap[i][0] = actualAngle
        gridMap[i][1] = distance
        if ((gridMap[i][1] < 10)):
            gridMap[i][1] = 0
        angle -= 15
        actualAngle -= 20
        pan_servo.write(angle)
        sleep(3)
    #calculates cartesian points
    for i in range(len(gridMap)):
        gridMap[i][0] = (gridMap[i][1] * math.cos(math.radians(gridMap[i][0])) + x_carD)
        gridMap[i][1] = (gridMap[i][1] * math.cos(math.radians(gridMap[i][0])) + y_carD)
    #determines if cartesian point is an object
    for i in range(len(gridMap)):
        if((gridMap[i][0] >= 0) and (gridMap[i][1] >= 0)):
           gridMap[i][0] = 1
           gridMap[i][1] = 1
        else:
           gridMap[i][0] = 0
           gridMap[i][1] = 0
    #imports the 10X2 numpy array and translates it into the 10x10 array
    for i in range(len(gridFinal)):
        if((gridMap[i][0]) == 1 and (gridMap[i][1]) == 1):
            gridFinal[y_carD][i] = 1


def main():
    # initial angle for pan
    pan_angle= 180
    print("Begin scanning")
    pan_servo.write(pan_angle)
    get_scan(pan_angle)
    #result map
    print(gridFinal)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
