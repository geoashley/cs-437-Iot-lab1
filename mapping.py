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


def get_scan( x_carD, y_carD):
    #replaces empty numpy array with [degree of angle, distance from sensor]
    actualAngle = 90
    pan_servo.set_angle(actualAngle)
    sleep(1)

    #print("gridMAp inital",gridMap)
    for i in range(len(gridMap)):
        pan_servo.set_angle(actualAngle)
        distance = us.get_distance()
        print("angles distance ",actualAngle, distance)
        gridMap[i][0] = actualAngle
        if (distance >0 and distance <= 25):
            gridMap[i][1] = distance
        actualAngle -= 18
        sleep(1)
   # print("gridMAp mid")
    #print(gridMap)
    #calculates cartesian points
    for i in range(len(gridMap)):
        gridMap[i][0] = int(gridMap[i][1] * math.sin(math.radians(gridMap[i][0])) + x_carD)
        gridMap[i][1] = int(gridMap[i][1] * math.cos(math.radians(gridMap[i][0])) + y_carD)
    #print("gridMAp cart")
    #print(gridMap)
    #determines if cartesian point is an object
    for i in range(len(gridMap)):
        if not ((gridMap[i][0] > 0) and (gridMap[i][1] > 0)):
           gridMap[i][0] = 0
           gridMap[i][1] = 0

    return gridMap

def main():
    # initial angle for pan
    pan_angle= 180
    print("Begin scanning")
    pan_servo.write(pan_angle)
    get_scan(pan_angle, 0, 0)
    #result map
    print(gridFinal)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
