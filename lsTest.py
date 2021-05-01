import RPi.GPIO as GPIO
import sys

leftIR = 3
rightIR = 2

GPIO.setup(leftIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(rightIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
  while(1):
    print("left sensor: ", GPIO.input(leftIR), " Right sensor: ", GPIO.input(rightIR))
    
except KeyboardInterrupt:
  GPIO.cleanup()
  sys.exit()
