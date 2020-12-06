import RPi.GPIO as GPIO
import time

servoPin = 12
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(channel, GPIO.OUT)

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)

p = GPIO.PWM(servoPin, 125)

p.start(2.5)

try:
  while True:
        motor_on(channel)
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


except KeyboardInterrupt:
    p.stop()
    motor_off(channel)
    time.sleep(1)
    GPIO.cleanup()
