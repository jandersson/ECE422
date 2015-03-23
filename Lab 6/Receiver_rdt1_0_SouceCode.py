# Server/Receiver
from  socket import *


localIP = '127.0.0.1'    # Local Host
localPORT = 8001         # Port for local process

#create a socket
rSocket = socket(AF_INET, SOCK_DGRAM)

#bind the socket with port number and IP address
rSocket.bind((localIP, localPORT))

#buffer to hold the message obtained from sender
buffer=b''

#Function extract the content of packet
def extract(packet):
    return packet

#Function to deliver data from transport layer to upper layer
def deliver_data(data):
    global buffer
    buffer=buffer+data
    return

#Function to receive the packet from sender
def rdt_rcv(packet):
    if not packet:
        return False
    else:
        return True

#main program
while True:
    packet=rSocket.recv(1024) # receive packet from sender through socket
    print('Received: ',packet)
    if packet:
        if rdt_rcv(packet): #check if packet is received
            data=extract(packet) #Extract the data from packet (there is only data in rdt1.0 and no checksum or seq number as it is error free)
            deliver_data(data) #Deliver data to upper layer
        print('Buffered: ',buffer)
                
rSocket.close() #close socket
