# Client/Sender
from  socket import *
from math import *

remoteIP = '127.0.0.1'   # Remote Host
remotePort = 8001        # Port for remote process

#message intended to send to Receiver
MSG=bytes("SIUC ECE422/553 Lab6-Sp15. We would like to use this message to implement a reliable transport protocol 1.0","utf-8")
MTU=20


#Function to make packet from the data sent by upper layer
def make_pkt(data):
    return data

#Function to send packet to Sender
def udt_send(packet):
    #create Socket
    sSocket = socket(AF_INET, SOCK_DGRAM)
    #Connect to receiver's socket
    sSocket.connect((remoteIP,remotePort))
    #send packet to Receiver
    sSocket.send(packet)
    #close Socket
    sSocket.close()
    return

#Function to send available data to create packet and send it to Receiver
def rdt_send(data):
    if not data:
        return False
    else:
        return True

#Main program
print(len(MSG))
fragNum=int(ceil(float(len(MSG))/float(MTU)))
print("Fragnmum=", fragNum)
for i in range(fragNum):
    data=MSG[i*MTU:(i+1)*MTU]   #Assigns 20 bytes of data from 'MSG' to 'data'
    if rdt_send(data):          #Calls function rdt_send to send data to lower layer
        packet=make_pkt(data)   #makes packet using data
        udt_send(packet)        #Calls function to send packet to receiver.
        print('Sent: ', packet)

