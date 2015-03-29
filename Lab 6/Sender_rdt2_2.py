# Sender
from socket import *
from math import *
from zlib import *
from random import *
from channel import *

# fill in start
# assign localIP address (Make sure to same variables)
localIP = '127.0.0.1'
# assign localPORT
localPORT = 9000
# assign remoteIP address
remoteIP = '127.0.0.1'
# assign remotePort remote process
remotePort = 8002
# fill in end

rSocket = socket(AF_INET, SOCK_DGRAM)
# fill in start
# Bind socket with localIP and localPort
# fill in end

MSG = b'SIUC ECE422/553 Lab6-Sp15. We would like to use this message to implement a reliable transport protocol 2.2'
MTU = 20

rdtVersion = 2.2  # [1.0,2.0,2.1,2.2,3.0]
corruptEnabled = True
corruptRatio = 0.3
dropEnabled = True
dropRatio = 0.3
seqNum = False  # Start from 0

# fill in start
# define function extract(packet)
def extract(packet):
    # calculate length of packet
    packet_length = len(packet)
    # return the data from packet excluding check sum (last bit of packet content)
    return packet[:packet_length-1]
# fill in end


# fill in start
# define function make_pkt() which takes arguments seqNum, data, checksum
def make_pkt(seqNum, data, checksum):
    # packet contains seqNum,data and checksum.
    # So assign required values to variable 'data' below. SeqNum is already assigned
    packet = str(int(seqNum)).encode()+ data + checksum # fill in start #fill in end
    # return packet
    return packet
# fill in end


# Function to send packet to receiver
def udt_send(packet):
    # fill in start
    # create a IPV4 UDP socket
    sSocket = socket(AF_INET, SOCK_DGRAM)
    # connect to sender socket using it's address and port number
    sSocket.connect((remoteIP, remotePort))
    # send packet
    sSocket.send(packet)
    # fill in end
    sSocket.close()
    print('Sent:', packet, '\n')
    return


# Function to make checksum from the data it obtained
def make_checksum(data):
    return chr(crc32(data)%127).encode()


# Function to check if packet received is corrupt
def corrupt(packet):
    global seqNum
    pLen = len(packet)
    if make_checksum(extract(packet)) == packet[(pLen-1):pLen]:
        return False
    else:
        return True


# Function to check if packet received is notcorrupt
def notcorrupt(packet):
    # Fill in start
    # define function notcorrupt which takes parameter packet
    global seqNum
    # get length of packet
    packet_length = len(packet)
    # check if obtained checksum matches with calculated checksum
    # (calcualte checksum by calling functions like extract and make_checksum)
    packet = extract(packet)
    make_checksum(packet)
    if make_checksum(extract(packet) == packet[(packet_length-1):packet_length]):
        return True
        # if it matches return true
    else:
        return False
    # Fill in end


def rdt_send(data):
    if not data:
        return False
    else:
        return True


def isACK(packet, seqNum):
    if packet[1:4] == b'ACK':
        if packet[0:1]==str(int(seqNum)).encode():
            return True
        else:
            return False
    else:
        return False


def rdt_rcv(packet):
    if len(packet)>0:
        return True
    else:
        return False

# Based on the data you got, come out how many packets need to be sent out
fragNum = int(ceil(float(len(MSG))/float(MTU)))

for i in range(fragNum):
    data = MSG[i*MTU:(i+1)*MTU]
    # FSM: Wait for the call from above
    if rdt_send(data): # Check rdt_send() to decide next FSM state
        checksum = make_checksum(str(int(seqNum)).encode()+data)
        sndpkt = make_pkt(seqNum, data, checksum)
        udt_send(sndpkt)
        # FSM: Wait for ACK or NAK
        while True:
            rcvpkt = channel('s', rdtVersion, corruptEnabled, corruptRatio, dropEnabled, dropRatio, rSocket.recv(1024))
            if rcvpkt:
                print('Received: ', rcvpkt)
            if rdt_rcv(rcvpkt) and notcorrupt(rcvpkt) and isACK(rcvpkt, seqNum):
                seqNum = not seqNum
                break
            else:
                udt_send(sndpkt)