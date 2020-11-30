import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

#pod is master
GPIO.setmode(GPIO.BCM)

csn=8
ce=17
mosi=10
miso=9
sck=11

#address 
pipes=[[0xe7, 0xe7, 0xe7, 0xe7, 0xe7, 0xe7],[0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio=NRF24(GPIO, spidev.SpiDev())
#CE0=>0, ce gpio pin number
radio.begin(0,ce)
#32 bytes
radio.setPayloadSize(32)
#channel number
radio.setChannel(0x60)

#higher data rate faster transmission, more risk of lost packet
radio.setDataRate(NRF24.BR_2MBPS) #2 mb/s speed
#power level amplification
radio.setPALevel(NRF24.PA_MIN)#minnimum power amplification
#auto acknowledgement
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
##everything above same as recv.py

radio.openReadingPipe(1, pipes[0])
radio.openWritingPipe(pipes[1])
#prints settiings for this code to verify that they are the same on the sender
radio.printDetails()
#while listening cannot write

refill=""
#setus up getStatus method
status=-1
sprev=-1
#GPIO pins for reed sensors
full=20
threequarters=25
half=26
quarter=18
#empty=6

GPIO.setup(full,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(half,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(threequarters,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(quarter,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(empty,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def getStatus():
    global status,sprev
    if GPIO.input(full):
        status=4
    elif GPIO.input(threequarters):
        status=3
    elif GPIO.input(half):
        status=2
    elif GPIO.input(quarter):
        status=1
#    elif GPIO.input(empty):
#        status=0
    if sprev!=status :
        sprev=status
    return status

def receiveData():
    radio.startListening()
    print("Ready to receive data..")
    
    #while not receiving sleep
    while not radio.available(0):
        time.sleep(1/100)
    
    #when receiving stop sleep
    receivedMessage=[]
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    
    print("Translating received message into unicode characters...")
    string=""
    for n in receivedMessage:
        if (n>=32 and n<=126):
            string +=char(n)
    print("Our slave sent us: {}" ,format(string))
    radio.stopListening()

def writeCom(value):
    message=list(value)
    radio.write(message)
    print("We sent message of {}".format(message))
    


#runs while battary above certain level--needs to be codeed
while True:
    command=""
    if getStatus()==1: #if using empty sensor use ==0
        command="EMPTY"
    if refill=="refill status_filling up":
        if getStatus()==4:
            command="status_full"
    if refill=="refill status_full":
        command=""
    writeCom(command)
    
    #Check if returned ackPL
    if radio.isAckPayloadAvailable():
        returnedPL=[]
        radio.read(returnedPL, radio.getDynamicPayloadSize())
        print("Our returned payload was {}".format(returnedPL))
        redfill=receiveData()
        print("received message: {}".format(refill))
        
    else:
        print("No payload received")
    #to avoid floodig receiver wait
    time.sleep(1)








