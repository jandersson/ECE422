# Receiver
from socket import *
from math import *
from zlib import *
from random import *
from channel import *

#fill in start

#assign localIP address (Make sure to same variables)
localIP = '127.0.0.1'
#assign localPORT
localPORT = 8002
#assign remoteIP address
remoteIP = '127.0.0.1'
#assign remotePort remote process
remotePort = 9000
# fill in end

rSocket = socket(AF_INET, SOCK_DGRAM)
# fill in start
# Bind socket with localIP and locolPort
rSocket.bind((localIP, localPORT))
# fill in end

buffer = b''

# Parameters to channel
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
    return packet[0:(packet_length-1)]
# fill in end


# Function to deliver data to upper layer
def deliver_data(data):
    global buffer
    buffer = buffer+data[1:]
    return


def make_checksum(data):
    return chr(crc32(data)%127).encode()


def corrupt(packet):
    pLen = len(packet)
    if make_checksum(packet[0:(pLen-1)]) == packet[(pLen-1):pLen]:
        return False
    else:
        return True


# fill in starts
# define function notcorrupt() which takes argument packet
def notcorrupt(packet):
    # calculate the length of packet
    pLen = len(packet)
    # if calculated checksum using data==checksum received
    if make_checksum(extract(packet)) == packet[(pLen-1):pLen]:
        return True
    # else
    else:
        return False
    # return false
# fill in ends


# fill in start
# define function make_pkt() which takes arguments seqNum, data, checksum
def make_pkt(seqNum, data, checksum):
    # packet contains seqNum,data and checksum. So assign required values to variable 'data' below.
    # SeqNum is already assigned
    packet = str(int(seqNum)).encode() + data + checksum
    return packet
    # return packet
# fill in end


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
    print('Sent:', packet)
    return


def rdt_rcv(packet):
    if not packet:
        return False
    else:
        return True


# Function to check if the received packet has seqNum 0
def has_seq0(packet):
    # fill in start
    # check if packet has Seq number 0.(Packet='SeqNUM+data+checksum', seqNUM is 1st byte)
    if packet[0:1] == b'0':
        return True
    # if present return true
    # fill in end
    else:
        return False


# Function to check if the received packet has seqNum 1
def has_seq1(packet):
    # fill in start
    # check if packet has Seq number 1.(Packet='SeqNUM+data+checksum', seqNUM is 1st byte)
    if packet[0:1] == b'1':
        return True
    # if present return true
    # fill in end
    # if packet[0:1]==b'1':
    #    return True
    else:
        return False


while True:
    # Assume the packet are affected by the underlying channel
    rcvpkt = channel('r', rdtVersion, corruptEnabled, corruptRatio, dropEnabled, dropRatio, rSocket.recv(1024))
    print('Received: ', rcvpkt)
    print('segNum:', int(seqNum))
    if rcvpkt:
        if seqNum:
            if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or has_seq0(rcvpkt)):
                checksum = make_checksum(str(int(not seqNum)).encode()+b'ACK')
                # Creating a checksum using seqNum and 'ACK'
                # fill in start
                sndpkt = make_pkt(not seqNum, b'ACK', checksum)
                # make a packet by calling make pkt with arguments seqNum, 'ACK', checksum.
                # (Note that seqNum type is boolean
                # and to send string in python 3 we send with following format: b'string',
                #  where b signifies bytes and
                # 'string' signifies the string you intend to send)
                # fill in end
                udt_send(sndpkt)
            if rdt_rcv(rcvpkt) and notcorrupt(rcvpkt) and has_seq1(rcvpkt):
                data = extract(rcvpkt)
                deliver_data(data)
                checksum = make_checksum(str(int(seqNum)).encode()+b'ACK')
                # fill in start
                sndpkt = make_pkt(seqNum, b'ACK', checksum)
                # make a packet by calling make pkt with arguments seqNum, 'ACK', checksum.
                # (Note that seqNum type is boolean and to send string in python 3 we send with following format:
                # b'string', where b signifies bytes and 'string' signifies the string you intend to send)
                # fill in end
                udt_send(sndpkt)
                seqNum = not seqNum
                
        else:
            if rdt_rcv(rcvpkt) and (corrupt(rcvpkt) or has_seq1(rcvpkt)):
                checksum = make_checksum(str(int(not seqNum)).encode()+b'ACK')
                # fill in start
                sndpkt = make_pkt(not seqNum, b'ACK', checksum)
                # make a packet by calling make pkt with arguments seqNum, 'ACK', checksum.
                # (Note that seqNum type is boolean and to send string in python 3 we send with following format:
                # b'string', where b signifies bytes and 'string' signifies the string you intend to send)
                # fill in end
                udt_send(sndpkt)
            if rdt_rcv(rcvpkt) and notcorrupt(rcvpkt) and has_seq0(rcvpkt):
                data = extract(rcvpkt)
                deliver_data(data)
                checksum = make_checksum(str(int(seqNum)).encode()+b'ACK')
                # fill in start
                sndpkt = make_pkt(seqNum, b'ACK', checksum)
                # make a packet by calling make pkt with arguments seqNum, 'ACK', checksum.
                # (Note that seqNum type is boolean and to send string in python 3 we send with following format:
                # b'string', where b signifies bytes and 'string' signifies the string you intend to send)
                # fill in end
                udt_send(sndpkt)                    
                seqNum = not seqNum
    print('Buffered: ', buffer)
rSocket.close()

# fill in start
# close receiver's packet

# fill in end
