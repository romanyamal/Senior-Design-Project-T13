import RPi.GPIO as GPIO
GPIO.setwarnings(False)

full=17
threequarters=27
half=16
quarter=12


GPIO.setmode(GPIO.BCM)

GPIO.setup(full,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(half,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(threequarters,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(quarter,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

status=-1
sprev=-1

while 1:

    if GPIO.input(full):
        status=4
        
    elif GPIO.input(threequarters):
        status=3
        
    elif GPIO.input(half):
        status=2
        
    elif GPIO.input(quarter):
        status=1

    if sprev!=status :
        print ('status=',status)
        sprev=status





