# Client/Sender
from socket import *
from math import *
from zlib import *
from random import *
#channel is a underlaying channel which introduces bit errors
from channel import *

localIP = '127.0.0.1'    # Local Host
localPORT = 9000         # Port for local process

remoteIP = '127.0.0.1'   # Remote Host
remotePort = 8002        # Port for remote process

rSocket = socket(AF_INET, SOCK_DGRAM) #create socket
rSocket.bind((localIP, localPORT)) #bind socket

MSG=b'SIUC ECE422/553 Lab6-Sp15. We would like to use this message to implement a reliable transport protocol 2.0'
MTU=20

rdtVersion=2.0 #[1.0,2.0,2.1,2.2,3.0] this for channel to know to introduce bit errors or drop packet in case of rdt3.0
corruptEnabled=True	#enabling bit error
corruptRatio=0.3	#Bit error ratio of 3 out of 10 packets
dropEnabled=True
dropRatio=0.3
seqNum=False 		#Start from 0

#Function to create packet which conatins data and checksum of the data
def make_pkt(data, checksum):
    packet=data+checksum
    return packet

#Function to send packet which contains data to receiver
def udt_send(packet):
    sSocket = socket(AF_INET, SOCK_DGRAM)	#Create socket
    sSocket.connect((remoteIP,remotePort))	#bind address of receiver
    sSocket.send(packet)			#send the created packet
    sSocket.close()				#close packet
    print('Sent:', packet)
    return

#Function to calculate checksum
def make_checksum(data):
    return chr(crc32(data)%127).encode()

#Function to send data from transport layer to lower layer for sending packet to recevier
def rdt_send(data):
    if not data:
        return False
    else:
        return True

#Function to check if received packet from receiver is 'ACK'
def isACK(packet):
    if packet[0:3]==b'ACK':
        return True
    else:
        return False

#Function to check if received packet from receiver is 'NAK'
def isNAK(packet):
    if packet[0:3]==b'NAK':
        return True
    else:
        return False

#Function to check if received packet has contents
def rdt_rcv(packet):
    if len(packet)>0:
        return True
    else:
        return False

#main program

# Base on the data you got, come out how many packets need to be sent out
fragNum=int(ceil(float(len(MSG))/float(MTU)))

for i in range(fragNum):
    data=MSG[i*MTU:(i+1)*MTU]	#Assigns 20 bytes of data from 'MSG' to 'data'

    #FSM: Wait for the call from above
    if rdt_send(data): #Check rdt_send() to decide next FSM state
        checksum=make_checksum(data)	#claculate check sum using data
        sndpkt=make_pkt(data,checksum)	#make packet using data and checksum
        udt_send(sndpkt)		#Send the created packet
    #FSM: Wait for ACK or NAK
    while True:
        rcvpkt=channel('s',rdtVersion,corruptEnabled,corruptRatio,dropEnabled,dropRatio,rSocket.recv(1024))
        if rcvpkt:
            print('Received: ',rcvpkt)
        #Check rdt_rcv() and isNAK() to decide next FSM state
        if (rdt_rcv(rcvpkt) and isNAK(rcvpkt)): 
            udt_send(sndpkt)
        #Check rdt_send() to isACK() to decide next FSM state
        if (rdt_rcv(rcvpkt) and isACK(rcvpkt)): 
            break

