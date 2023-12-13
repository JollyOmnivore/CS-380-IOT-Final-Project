from djitellopy import Tello
import threading
import time
import serial
myCommPort = serial.Serial('COM6', 9600)

tello = Tello()

tello.connect()







# for testing comands from adrino with using drone
# while True:
#     x = myCommPort.readline()
#     x = str(x)
#     x = x[2:]
#     x = x[0: len(x) - 5]
#     print(x)
#     if x == "q":
#         break

def forward():
    tello.move_forward(150)


def back():
    tello.move_back(150)


def left():
    tello.move_left(150)


def right():
    tello.move_right(150)


def up():
    tello.move_up(100)


def down():
    tello.move_down(50)


def land():
    tello.land()


def battery():
    return tello.get_battery()


def flip():
    tello.flip_forward()


def rotateCounterClockwise():
    tello.rotate_counter_clockwise(90)


def rotateClockwise():
    tello.rotate_clockwise(90)



def takeoff():
    tello.takeoff()


def print_data():
    while tello.is_flying:
        print("Battery: " + str(tello.get_battery()) + " %")
        print("Height: " + str(tello.get_height()) + " cm")
        print("Drone Temp: " + str(tello.get_temperature()) + " Fahrenheit")
        time.sleep(5)


tello.takeoff()
data = threading.Thread(target=print_data)
print(tello.get_battery())

while True:
    droneCommand = myCommPort.readline()
    droneCommand = str(droneCommand)
    droneCommand = droneCommand[2:]
    droneCommand = droneCommand[0: len(droneCommand) - 5]
    if droneCommand == "TAKE OFF":
        takeoff()
        data.start()
    while tello.is_flying:
        droneCommand = myCommPort.readline()
        droneCommand = str(droneCommand)
        droneCommand = droneCommand[2:]
        droneCommand = droneCommand[0: len(droneCommand) - 5]
        print(droneCommand)
        if droneCommand == "FLY FORWARD":
            forward()
        elif droneCommand == "FLY BACKWARDS":
            back()
        elif droneCommand == "FLY LEFT":
            left()
        elif droneCommand == "FLY RIGHT":
            right()
        elif droneCommand == "q":
            land()
        elif droneCommand == "UP":
            up()
        elif droneCommand == "DOWN":
            down()
        elif droneCommand == "flip":
            flip()
        elif droneCommand == "ROTATE COUNTER CLOCKWISE":
            rotateCounterClockwise()
        elif droneCommand == "ROTATE CLOCKWISE":
            rotateClockwise()
        elif droneCommand == "LAND":
            land()
            break

data.join()

