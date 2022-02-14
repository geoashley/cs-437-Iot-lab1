## CS-437-IOT LAB-1

### Drive  ###
````drive.py```` is the main program that uses the ultrasonic sensor to detect obstacles that come within several centimeters of your car's front bumper. When your car gets within that obstacle, it should stop, choose another random direction, back up and turn, and then move forward in the new direction.

### Navigation  ###
````navigation.py```` is the main program that orchestrates the navigation of the car.It first initializes the global variables for communicating between threads. It then starts the object detection routine in a separate thread that runs in the background. If a stop sign is detected the car stops for 2 seconds. The main program initializes a 50x50 grid and tried to navigate from a preset starting coordinate to a ‘goal’ coordinate. The main loop iterates until the car reaches the goal

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