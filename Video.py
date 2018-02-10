#!/usr/bin/env python

"""
Captured TCP Traffic:

1: video negotiation??
	<< connection to 8080 0x0f
	>> 55:44:50:37:32:30:50 "UDP720P"
	<< 0x28
	>> 56:32:2e:33:2e:34 "V2.3.4"

2: handshake completed for port 8888, nothing more
4: ??
    << 00:01:02:03:04:05:06:07:08:09:25:25
    >> 6e:6f:61:63:74:0d:0a "noact"

5:connection reset and APP sends 00:01:02:03:04:05:06:07:08:09:28:28 seeming to start video stream.
<< 00:01:02:03:04:05:06:07:08:09:28:28
>> ~1500 byte packets every
"""

import socket
import select
from time import sleep

start = '000102030405060708092525'.decode('hex')
one = '0f'.decode('hex')
two = '28'.decode('hex')

# Start connection
# IPADDR = '172.16.10.1'
IPADDR = '127.0.0.1'
TCPPORTNUM = 8888
UDPPORTNUM = 8080
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
connection.connect((IPADDR, TCPPORTNUM))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
s.connect((IPADDR, UDPPORTNUM))
s.send(one)
print(s.recv(100))
s.send(two)
print(s.recv(100))

connection.send(start)

looping = True
buff = ''
while looping:

    buff = connection.recv(1000)
    print buff.strip("\n").decode('hex')


connection.close()
