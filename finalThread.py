import RPi.GPIO as GPIO
import sys #to terminate program/stop executing
import time
import threading

GPIO.setwarnings(False)
GPIO.cleanup()

#GPIO pins for level sensor on tank
full= 24
threequarters=27
half=23
quarter= 22

#GPIO pins for motor
motor1A = 4
motor1B = 14
motor2A = 17
motor2B = 18
enable1 = 26
enable2 = 20

#GPIO pins for line senor
leftIR = 3
rightIR = 2
# global leftIR 
# global rightIR
# leftIR = False
# rightIR = False

#GPIO pins for servo motor
servoP = 12

#GPIO pins for water pump
waterP = 19

#Using GPIO numbers instead of Board configuration
GPIO.setmode(GPIO.BCM)

#Setup pins for tank sensors to have less noise interference
GPIO.setup(full,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(half,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(threequarters,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(quarter,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO setup for motor
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(enable1, GPIO.OUT)
GPIO.setup(enable2, GPIO.OUT)

#GPIO setup for line senor
GPIO.setup(leftIR, GPIO.IN)
GPIO.setup(rightIR, GPIO.IN)

#GPIO setup for servo motor
GPIO.setup(servoP, GPIO.OUT)

#GPIO setup for water pump
GPIO.setup(waterP, GPIO.OUT)


global actionP
global actionS
global status
global sprev
global p
global terminate
terminate = 0
        
def level():
    while(terminate == 0):
        time.sleep(1)
        print("level")
        global sprev
        global status
        if GPIO.input(full):
            status=4
            
        elif GPIO.input(threequarters):
            status=3
            
        elif GPIO.input(half):
            status=2
            
        elif GPIO.input(quarter):
            status=1

        if (sprev != status and sprev != -1):
            print ('status=',status)
            sprev = status
        
        elif(sprev == -1):
            sprev = 0
              
class Motor:
    #initail state of motor
    def __init__(self, pin, frequency):
        self.pin = pin
        self.pm=GPIO.PWM(pin,frequency)
        self.pm.start(0)
    
    def speed(self, dutyCycle):
        #code to move motor forward
        self.pm.ChangeDutyCycle(dutyCycle)
        
    def stop(self):
        #code to stop motor
        self.pm.start(0)

        
def pump():
    #if 1 turn on pump
    if(actionP == 1):
        GPIO.output(waterP, GPIO.HIGH)
        print("Pump started")
    #else turn off pump and  code
    elif(actionP == 0):
        GPIO.output(waterP, GPIO.LOW)

def servoF():
        #check tank level if more than 1/4 full turn on spray nozzle & pump
    while(terminate == 0):
        time.sleep(1)
        #print("servo")
        if(status > 1):
            actionP = 1
            pump()
            #print("Servo started")
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(1)
            p.ChangeDutyCycle(5)
            time.sleep(0.1)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.1)
            p.ChangeDutyCycle(10)
            time.sleep(0.1)
            p.ChangeDutyCycle(12.5)
            time.sleep(0.1)
            p.ChangeDutyCycle(10)
            time.sleep(0.1)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.1)
            p.ChangeDutyCycle(5)
            time.sleep(0.1)
            p.ChangeDutyCycle(2.5)
            time.sleep(0.1)
            
        #else turn off servo code
        elif(actionS == 0):
            GPIO.output(servoP, GPIO.LOW)
            actionP = 0
            pump()

def mobility():
    while(terminate == 0):
        mot1.speed(25)
        mot2.speed(25)
        time.sleep(1)
        #print("motors")
        #device moves straight
        if(GPIO.input(rightIR) == True and GPIO.input(leftIR) == True):
            #print("Driving straight")
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, False)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, False)
            
        #device turns right
        elif(GPIO.input(rightIR) == False and GPIO.input(leftIR) == True):
            #print("Turning right")
            mot1.speed(20) #Motor 1 spins backward
            mot2.speed(85)
            GPIO.output(motor1A, False)
            GPIO.output(motor1B, True)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, False)
                
        #device turns left
        elif(GPIO.input(rightIR) == True and GPIO.input(leftIR) == False):
            #print("Turning left")
            mot2.speed(20) #Motor 2 spins backwards
            mot1.speed(85)
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, False)
            GPIO.output(motor2A, False)
            GPIO.output(motor2B, True)
        
        #device stops moving
        elif(GPIO.input(rightIR) == False and GPIO.input(leftIR) == True):
            #print("Device stopped")
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, True)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, True)

def refill():
    #stop for refill
    #wait for predefied time it takes to refill
    pass

#setup current items
mot1 = Motor(enable1, 1000)
mot2 = Motor(enable2, 1000)
p=GPIO.PWM(servoP,50)
p.start(0)
servo1=threading.Thread(target=servoF, name='servo1')
level1=threading.Thread(target=level, name='level1')
mobility1=threading.Thread(target=mobility, name='mobility1')

#main code that runs the loop
try:
    actionP=0
    actionS=0
    status=0
    sprev=-1
    level1.start()
    mobility1.start()
    servo1.start()
#     while 1:
#         key=input("Enter: ")
#         key = int(key)
#         if(key == 1):
#             rightIR = True
#         elif(key == 2):
#             leftIR = True
#         elif(key == 3):
#             time.sleep(1)
#             rightIR = False
#             leftIR = False


except KeyboardInterrupt:
    terminate=1
    level1.join()
    mobility1.join()
    servo1.join()
    GPIO.cleanup()
    print("Keyboard interrupt ended program")
    time.sleep(1)
    sys.exit() #Causes error only when cntr^c clicked twice fast before program exits




