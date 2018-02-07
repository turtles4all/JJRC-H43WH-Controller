import socket
from time import sleep
"""
ff:08:00:3f:40:3f:10:10:10:01:08 %60
ff:08:00:3f:40:3f:10:10:10:02:07 %100
ff:08:7e:3f:40:3f:90:10:10:00:0b %30 and auto launch
ff:08:7e:3f:40:3f:90:10:10:02:09 %100 and auto launch
ff:08:7e:3f:40:3f:90:10:10:42:c9 start props
ff:08:f8:30:40:3f:90:10:10:02:9e Launch ??
ff:08:7e:3f:40:3f:90:10:10:82:89 auto land / stop of not launched
"""


# The IP of the quadcopter plus the UDP port it listens to for control commands
IPADDR = '172.16.10.1'
UDPPORTNUM = 8080
TCPPORTNUM = 8888


INIT = '26e207000002000000030000000600000015000000070000002c000000'.decode('hex')
START = 'ff08003f403f1010100009'.decode('hex') 
ARM = 'ff087e3f403f9010100209'.decode('hex')
SPINUP = 'ff087e3f403f90101042c9'.decode('hex')
LAND = 'ff087e3f403f9010108289'.decode('hex')
LAUNCH = 'ff08f830403f901010029e'.decode('hex')
CAL = 'ff087e3f403fd0101002c9'.decode('hex')
BADLAUNCH = 'ff08f830403f9010100200'.decode('hex')

# UDP connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# TCP connection
t = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# connect the socket
s.connect((IPADDR, UDPPORTNUM))
 
# send a series of commands
for n in range(0,10): 
    print("sending INIT")
    s.send(INIT)
    sleep(0.05) 
t.connect((IPADDR, TCPPORTNUM))
for n in range(0,40): 
    print("sending Start")
    s.send(START)
    sleep(0.05)
s.send(INIT)
for n in range(0,10): 
    print("sending Calibrate")
    s.send(CAL)
    sleep(0.05)
s.send(INIT)
sleep(2)
s.send(INIT)
for n in range(0,40): 
    print("sending ARM")
    s.send(ARM)
    sleep(0.05)
s.send(INIT)
for n in range(0,40): 
    print("sending SPINUP")
    s.send(SPINUP)
    sleep(0.05)
s.send(INIT)
for n in range(0,40): 
    print("sending LAUNCH")
    s.send(LAUNCH)
    sleep(0.05)
s.send(INIT)
#land not working
for n in range(0,40): 
    print("sending LAND")
    s.send(LAND)
    sleep(0.05)

s.send(INIT)
# close the socket
t.close()
s.close()
