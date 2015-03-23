from random import *
from math import *

def channel(role,rdtVersion,corruptEnabled,corruptRatio,dropEnabled,dropRatio,packet):

    if role=='r':
        verIndex=1
    elif role=='s':
        verIndex=2
        
    if rdtVersion>verIndex:
        if corruptEnabled:
            pLen=len(packet)
            corruptEvent=randint(1,ceil(3/corruptRatio))
            
            if corruptEvent==1:
                print('Channel: Corruption at the beginning')
                packet=b'x'+packet[1:pLen]
            elif corruptEvent==2:
                print('Channel: Corruption at the middle')
                packet=packet[0:1]+b'x'+packet[2:pLen]
            elif corruptEvent==3:
                print('Channel: Corruption at the end')
                packet=packet[0:(pLen-1)]+b'x'
            else:
                print('Channel: No corruption')
                
    if rdtVersion>2.2:
        if dropEnabled:
            dropEvent=randint(1,ceil(3/corruptRatio))
            if dropEvent<3:
                print('Channel: Packet is dropped!')
                packet=b''
            else:
                print('Channel: No dropped packet!')
            
    return packet
