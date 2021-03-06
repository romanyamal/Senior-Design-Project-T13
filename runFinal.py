import RPi.GPIO as GPIO
import sys #to terminate program/stop executing
import time

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

#GPIO pins for servo motor
servoPin = 12

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
GPIO.setup(servoPin, GPIO.OUT)

#GPIO setup for water pump
GPIO.setup(waterP, GPIO.OUT)

    
class Tank:
    #Initial status for tank
    def __init__(self):
        self.status=0
        self.sprev=-1
        
    def level(self):
        if GPIO.input(full):
            self.status=4
            
        elif GPIO.input(threequarters):
            self.status=3
            
        elif GPIO.input(half):
            self.status=2
            
        elif GPIO.input(quarter):
            self.status=1

        if (self.sprev != self.status and self.sprev != -1) :
            print ('status=',self.status)
            self.sprev = self.status
            return self.status
        
        elif(self.sprev == -1):
            self.sprev = 0
            return self.sprev
            
        else:
            return self.status
            
class Motor:
    #initail state of motor
    def __init__(self, pin, frequency):
        self.pin = pin
        self.p=GPIO.PWM(pin,frequency)
        self.p.start(0)
    
    def speed(self, dutyCycle):
        #code to move motor forward
        self.p.ChangeDutyCycle(dutyCycle)
        
    def stop(self):
        #code to stop motor
        self.p.start(0)

class SprayNozzle:
    #initial setup of sprayNozzle
    def __init__(self, pin, frequency):
        self.pin = pin
        self.p = GPIO.PWM(pin, frequency)
        self.p.start(2.5)
        
    def pump(self,action):
        #if 1 turn on pump
        if(action == 1):
            GPIO.output(self.pin, GPIO.HIGH)
            #print("Pump started")
        #else turn off pump and  code
        elif(action == 0):
            GPIO.output(self.pin, GPIO.LOW)
        #else if unknown command print unknown command
        else:
            print("Wrong value entered for pump")

    def servoF(self, action):
        #if 1 turn on servo code
        if(action == 1):
            #print("Servo started")
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(1)
            self.p.ChangeDutyCycle(5)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(7.5)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(10)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(12.5)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(10)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(7.5)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(5)
            time.sleep(0.1)
            self.p.ChangeDutyCycle(2.5)
            time.sleep(0.1)
            
        #else turn off servo code
        elif(action == 0):
            GPIO.output(self.pin, GPIO.LOW)
        #else if unknown command print unknown command
        else:
            print("Wrong value entered for servoF")

def refill():
    #stop for refill
    #wait for predefied time it takes to refill
    pass


#setup current items
bucket = Tank()
mot1 = Motor(enable1, 8000)
mot2 = Motor(enable2, 8000)
nozzle = SprayNozzle(servoPin, 50)
currentMode=0
start=0
continueM=0
#main code that runs the loop
try:
    while 1:
        #motors start at duty cycle 10
        mot1.speed(6)
        mot2.speed(6)
        #print(bucket.level())
        #device moves straight
        if(GPIO.input(rightIR) == True and GPIO.input(leftIR) == True):
            #print("Driving straight")
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, False)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, False)
            currentMode=1
            
        #device turns right
        elif(GPIO.input(rightIR) == False and GPIO.input(leftIR) == True):
            #print("Turning right")
            mot1.speed(34) #Motor 1 spins backward
            mot2.speed(84)
            GPIO.output(motor1A, False)
            GPIO.output(motor1B, True)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, False)
            currentMode=1
            
        #device turns left
        elif(GPIO.input(rightIR) == True and GPIO.input(leftIR) == False):
            #print("Turning left")
            mot2.speed(34) #Motor 2 spins backwards
            mot1.speed(84)
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, False)
            GPIO.output(motor2A, False)
            GPIO.output(motor2B, True)
            currentMode=1
        
        #device stops moving
        elif(GPIO.input(rightIR) == False and GPIO.input(leftIR) == True):
            #print("Device stopped")
            GPIO.output(motor1A, True)
            GPIO.output(motor1B, True)
            GPIO.output(motor2A, True)
            GPIO.output(motor2B, True)
            currentMode=0
            
        #check tank level if more than 1/4 full turn on spray nozzle & pump
        if(bucket.level() > 1 and currentMode == 1):
            #Record time counter while running
            if(start=0 and continueM !=0)
                continueM=continueM-1
                
            if(continueM == 0)
                start=start+1
                nozzle.pump(1)
                nozzle.servoF(1)
            
        #if at 1/4 or less turn off pump and servo for spray nozzle
        else:
            continueM=start
            start=0
            nozzle.pump(0)
            nozzle.servoF(0)


except KeyboardInterrupt:
    GPIO.cleanup()
    print("Keyboard interrupt ended program")
    time.sleep(1)
    sys.exit() #Causes error only when cntr^c clicked twice fast before program exits


