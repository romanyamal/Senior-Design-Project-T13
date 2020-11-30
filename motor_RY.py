import RPi.GPIO as GPIO 
import time

GPIO.setwarnings(False)

in1=23
in2=24

forward=25
backward=21

en=20

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.setup(forward,GPIO.IN)
GPIO.setup(backward,GPIO.IN)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(en,GPIO.HIGH)

while 1:
    if GPIO.input(forward):
        GPIO.output(in1,GPIO.HIGH)
    elif GPIO.input(backward):
        GPIO.output(in2,GPIO.HIGH)
    elif GPIO.input(forward) & GPIO.input(backward):
        break
    else:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
    
GPIO.output(en,GPIO.LOW)
GPIO.cleanup()
        




