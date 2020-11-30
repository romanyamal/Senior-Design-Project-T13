import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

#refill station is slave 
GPIO.setmode(GPIO.BCM)

#gpio for transmitter
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

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
#prints settiings for this code to verify that they are the same on the sender
radio.printDetails()

#refill state to send and receive..
state=""

radio.startListening()

def checkStatus():
    if status==4:
        state= "full"
        print("Pod retardant level full.")
        #****send to pod status full
    return state
    

def sendData(ID, value):
    radio.stopListening()
    time.sleep(0.25)
    message=list(ID) + list(value)
    print("about to send message.")
    radio.write(message)
    print("Sent data.")
    radio.startListening()
    
def refill(action):
    if(action=="start"):
        #code to open refill servo
        print("Starting refill...")

    if(action=="stop"):
        #code to close refill valve
        print("Refill done.")
    
while True:
    ackPL=[1]
    radio.writeAckPayload(1,ackPL, len(ackPL)) 
    while not radio.available(0):
        time.sleep(1/100)
        
    receivedMessage=[]
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))
    #sends in bytes 8bit-byte only values can be sent integers from 0-255
    
    print("Translating received message into unicode characters...")
    string=""
    for n in receivedMessage:
        #Decode into standard unicode set
        if(n>=32 and n<=126):
            string+=char(n)
    print(string)
    
    #want to react to command from master
    command=string
    if command=="EMPTY":
        refill("start")
        state= "filling up"
        sendData("refill status_", state)
    if command=="status_full":
        refill("stop")
        state="full"
        sendData("refill status_",state)
    #reset command
    command=""
    
    radio.writeAckPayload(1, ackPL, len(ackPL))
    print("loaded payload reply of {}".format(ackPL))







