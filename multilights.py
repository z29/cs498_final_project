import RPi.GPIO as GPIO
import time

OUTER_AIRLOCK = 17
PRESSURE = 18
INNER_AIRLOCK = 22
SERVO = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(OUTER_AIRLOCK, GPIO.OUT)
GPIO.setup(PRESSURE, GPIO.OUT)
GPIO.setup(INNER_AIRLOCK, GPIO.OUT)
airlock_1 = GPIO.PWM(SERVO, 50)
airlock_1.start(0)

def door(airlock, state):
    airlock.ChangeDutyCycle(state)

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

    while True:
        n = input("What would you like to do?\n1)Open Outer Airlock\n2)Close Outer Airlock\n3)Open Inner Airlock\n4)Close Inner Airlock\n5)Quit\n\n")
        if n == 5 or n == "quit":
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
                door(airlock_1,12)
        elif n == 2 :
            OUTER_OPEN = False
            print("CLOSING OUTER AIRLOCK")
            time.sleep(2)
            door(airlock_1,7)
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
                door(airlock_1,12)
        elif n == 4 :
            INNER_OPEN = False
            print("CLOSING INNER AIRLOCK")
            time.sleep(2)
            door(airlock_1,7)
            airlock(INNER_AIRLOCK, INNER_OPEN)
            
    
except Exception as e:
    print("error= ",e)
finally:
    print("Done")
    airlock_1.stop()
    GPIO.cleanup()
