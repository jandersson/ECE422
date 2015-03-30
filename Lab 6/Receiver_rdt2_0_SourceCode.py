# Server/Receiver
from socket import *
from math import *
from zlib import *
from random import *
# channel is a underlaying channel which introduces bit errors
from channel import *

localIP = '127.0.0.1'    # Local Host
localPORT = 8002         # Port for local process

remoteIP = '127.0.0.1'   # Remote Host
remotePort = 9000        # Port for remote process

rSocket = socket(AF_INET, SOCK_DGRAM)
rSocket.bind((localIP, localPORT))

buffer=b''


rdtVersion = 2.0  # [1.0,2.0,2.1,2.2,3.0] this for channel to know to introduce bit errors or drop packet in case of rdt3.0
corruptEnabled = True	#enabling bit error
corruptRatio = 0.3	#Bit error ratio of 3 out of 10 packets
dropEnabled = True
dropRatio = 0.3
seqNum = False 		#Start from 0

#Function to extract content of packet i.e data only
def extract(packet):
    pLen=len(packet)
    return packet[0:(pLen-1)] #return data by removing check sum

#Function to deliver data to upper layer
def deliver_data(data):
    global buffer
    buffer=buffer+data
    return

#Function to calculate checksum
def make_checksum(data):    
    return chr(crc32(data)%127).encode()


#Function to check if received packet is corrupt
def corrupt(packet):
    pLen=len(packet)
    if make_checksum(extract(packet))==packet[(pLen-1):pLen]:
    # make checksum using data and compare it with received check sum
        return False
    else:
        return True

#Function to check if received packet in not corrupt. It is same as previous function, but written for your understanding to compare with finite state machine diagrams in the textbook
def notcorrupt(packet):
    pLen=len(packet)
    if make_checksum(extract(packet))==packet[(pLen-1):pLen]:
        return True
    else:
        return False

#Function to create packet which conatins information to sender for Ex: 'ACK' or 'NAK'. 
def make_pkt(payload):
    return payload	#During making packet we send either 'ACK' or 'NAK' due to assumption in rdt2.0 that there is no bit errors from receiver to sender

#Function to send acknowledge packet to sender
def udt_send(packet):
    sSocket = socket(AF_INET, SOCK_DGRAM)
    sSocket.connect((remoteIP,remotePort))
    sSocket.send(packet)
    sSocket.close()
    return

#Function to receive packet from sender
def rdt_rcv(packet):
    if not packet:
        return False
    else:
        return True      

#main program
while True:
    ## Assume the packet are affected by the underlying channel
    rcvpkt = channel('r', rdtVersion, corruptEnabled,corruptRatio,dropEnabled,dropRatio, rSocket.recv(1024))
    print('Received: ',rcvpkt)
    if rcvpkt:
        if (rdt_rcv(rcvpkt) and corrupt(rcvpkt)): #once packet is received check if packet is corrupt
            sndpkt=make_pkt(b'NAK') 	#if packet is corrupt send 'NAK' to sender
            udt_send(sndpkt)

        if (rdt_rcv(rcvpkt) and notcorrupt(rcvpkt)):
            data=extract(rcvpkt)	#if packet is not corrupt send 'ACK' to sender
            deliver_data(data)
            sndpkt=make_pkt(b'ACK')
            udt_send(sndpkt)
        
        print('Buffered: ',buffer)

                
rSocket.close()
