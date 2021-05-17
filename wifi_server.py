import socket
import RPi.GPIO as GPIO
import time

HOST = "192.168.1.42" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


########GPIO########
OUTER_AIRLOCK = 17
INNER_AIRLOCK = 22
OUTER_DOOR = 4
INNER_DOOR = 26
ROOM_1 = 19
ROOM_2 = 13
ROOM_3 = 6
PRESSURE = 18

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
####################

########Bools#######
room_1_on = False
room_2_on = False
room_3_on = False
outer_open = False
inner_open = False
####################

#####Functions######
def led(gpio,state):
    print("led, ",gpio,",",state)
    GPIO.output(gpio,state)
    
def pressure():
    global PRESSURE
    for i in range(5):
        print("EQUILIZING PRESSURE")
        GPIO.output(PRESSURE,True)
        time.sleep(0.5)
        GPIO.output(PRESSURE,False)
        time.sleep(0.5)
        
def door(airlock, state):
    if(state):
        airlock.ChangeDutyCycle(12)
    else:
        airlock.ChangeDutyCycle(7)
####################


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                data = data.decode("UTF-8").strip()
                print(data)     
                if data == "5":
                    room_1_on = not room_1_on
                    led(ROOM_1,room_1_on)
                elif data == "6":
                    room_2_on = not room_2_on
                    led(ROOM_2,room_2_on)
                elif data == "7":
                    room_3_on = not room_3_on
                    led(ROOM_3,room_3_on)
                elif data == "1":
                    outer_open = not outer_open
                    if outer_open:
                        pressure()
                    led(OUTER_AIRLOCK,outer_open)
                    time.sleep(2)
                    door(door_1,outer_open)
                elif data == "2":
                    inner_open = not inner_open
                    if inner_open:
                        pressure()
                    led(INNER_AIRLOCK,inner_open)
                    time.sleep(2)
                    door(door_2,inner_open)
                    

    except Exception as e:
        print("error= ",e)
        GPIO.cleanup()
        client.close()
        s.close()
    finally:
        print("Done")
        GPIO.cleanup()
        client.close()
        s.close()
