## CS-437-IOT LAB-1

drive.py is the main program that uses the ultrasonic sensor to detect obstacles that come within several centimeters of your car's front bumper. When your car gets within that obstacle, it should stop, choose another random direction, back up and turn, and then move forward in the new direction.

## Build

````
make zip
````
## Copy to Raspberry pi

````
scp /path/to/car.zip pi@<ipaddress>:
````
## Unzip

````
unzip car.zip -d car
````
## Run Drive

````
make run
````

## Run Navigate

````
make navigate
````