import RPi.GPIO as GPIO
import time

OUTER_AIRLOCK = 17
PRESSURE = 18
INNER_AIRLOCK = 22
OUTER_DOOR = 4
INNER_DOOR = 26
ROOM_1 = 19
ROOM_2 = 13
ROOM_3 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(OUTER_DOOR, GPIO.OUT)
GPIO.setup(OUTER_AIRLOCK, GPIO.OUT)
GPIO.setup(PRESSURE, GPIO.OUT)
GPIO.setup(INNER_AIRLOCK, GPIO.OUT)
GPIO.setup(INNER_DOOR, GPIO.OUT)
GPIO.setup(ROOM_1, GPIO.OUT)
GPIO.setup(ROOM_2, GPIO.OUT)
GPIO.setup(ROOM_3, GPIO.OUT)
door_1 = GPIO.PWM(OUTER_DOOR, 50)
door_1.start(0)
door_2 = GPIO.PWM(INNER_DOOR, 50)
door_2.start(0)

def door(airlock, state):
    airlock.ChangeDutyCycle(state)

def main_room():
    GPIO.output(PRESSURE, True)
    time.sleep(5)
    GPIO.output(PRESSURE, False)

def airlock(gpio,airlock_open):
    GPIO.output(gpio,airlock_open)

def equalizingPressure():
    global PRESSURE
    for i in range(5):
        print("EQUILIZING PRESSURE")
        GPIO.output(PRESSURE,True)
        time.sleep(0.5)
        GPIO.output(PRESSURE,False)
        time.sleep(0.5)

def airlocks_safe(outer, inner):
    if outer == False and inner == False:
        return True
    else:
        return False

try:
    OUTER_OPEN = False
    INNER_OPEN = False
    ROOM_1_ON = False
    ROOM_2_ON = False
    ROOM_3_ON = False
    while True:
        n = input("What would you like to do?\n1)Open Outer Airlock\n2)Close Outer Airlock\n3)Open Inner Airlock\n4)Close Inner Airlock\n5)Room 1\n6)Room 2\n7)Room 3\n8)Quit\n\n")
        if n == 8 or n == "quit":
            break
        elif n == 1 :
            print("reached 1")
            if not (airlocks_safe(OUTER_OPEN, INNER_OPEN)):
                print("!!!WARNING!!! BOTH AIRLOCKS MUST BE CLOSED")
            else:
                equalizingPressure()
                OUTER_OPEN = True
                airlock(OUTER_AIRLOCK, OUTER_OPEN)
                print("OPENING OUTER AIRLOCK")
                time.sleep(2)
                door(door_1,12)
        elif n == 2 :
            OUTER_OPEN = False
            print("CLOSING OUTER AIRLOCK")
            time.sleep(2)
            door(door_1,7)
            airlock(OUTER_AIRLOCK, OUTER_OPEN)
        elif n == 3 :
            if not (airlocks_safe(OUTER_OPEN, INNER_OPEN)):
                print("!!!WARNING!!! BOTH AIRLOCKS MUST BE CLOSED")
            else:
                equalizingPressure()
                INNER_OPEN = True
                airlock(INNER_AIRLOCK, INNER_OPEN)
                print("OPENING INNER AIRLOCK")
                time.sleep(2)
                door(door_2,12)
        elif n == 4 :
            INNER_OPEN = False
            print("CLOSING INNER AIRLOCK")
            time.sleep(2)
            door(door_2,7)
            airlock(INNER_AIRLOCK, INNER_OPEN)
        elif n == 5 :
            ROOM_1_ON = not ROOM_1_ON
            airlock(ROOM_1, ROOM_1_ON)
        elif n == 6 :
            ROOM_2_ON = not ROOM_2_ON
            airlock(ROOM_2, ROOM_2_ON)
        elif n == 7 :
            ROOM_3_ON = not ROOM_3_ON
            airlock(ROOM_3, ROOM_3_ON)
            
    
except Exception as e:
    print("error= ",e)
finally:
    print("Done")
    door_1.stop()
    door_2.stop()
    GPIO.cleanup()
