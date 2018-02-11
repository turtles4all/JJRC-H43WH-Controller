#!/usr/bin/env python

"""
Controls:
	W/A/S/D - Up, Down, Rotate Left, Rotate Right
	Arrow keys 
	Up/Down/Left/Right - Forward, Bacwards, Left, Right
	
	Commands / Modes:
	E-Stop - ESC
	Launch - Page Up
	Land - Page Down
"""

import socket
import pygame
from pygame.locals import *
from time import sleep

# Key mappings
Forward_key = K_UP
Back_key    = K_DOWN
Left_key    = K_LEFT
Right_Key   = K_RIGHT
Up_key      = K_w
Down_Key    = K_s
RotateL_key = K_a
RotateR_key = K_d
# Command Keys
Launch_key  = K_PAGEUP
Land_key    = K_PAGEDOWN
Cal_key     = K_F1
Exit_key    = K_ESCAPE
# trim keys
F_trim_k   = K_KP8
B_trim_k   = K_KP2
L_trim_k   = K_KP4
R_trim_k   = K_KP5
# Speed
Inc_speed_k = K_KP_PLUS
Dec_speed_k = K_KP_MINUS
Turbo_k = K_F12

INIT = '26e207000002000000030000000600000015000000070000002c000000'.decode('hex')
START = 'ff08003f403f1010100009'.decode('hex')
ARM = 'ff087e3f403f9010100209'.decode('hex')
SPINUP = 'ff087e3f403f90101042c9'.decode('hex')
LAND = 'ff087e3f403f9010108289'.decode('hex')
LAUNCH = 'ff08f830403f901010029e'.decode('hex')
CAL = 'ff087e3f403fd0101002c9'.decode('hex')


def start():
    for n in range(0, 10):
        print("sending INIT")
        s.send(INIT)
        sleep(0.05)
    t.connect((IPADDR, TCPPORTNUM))
    for n in range(0, 10):
        print("sending Start")
        s.send(START)
        sleep(0.05)
    s.send(INIT)

def calibrate():
    for n in range(0, 10):
        print("sending Calibrate")
        s.send(CAL)
        sleep(0.05)
    s.send(INIT)
    sleep(2)
    s.send(INIT)

def launcher():
    for n in range(0, 10):
        print("sending ARM")
        s.send(ARM)
        sleep(0.05)
    s.send(INIT)
    for n in range(0, 10):
        print("sending SPINUP")
        s.send(SPINUP)
        sleep(0.05)
    s.send(INIT)
    sleep(.5)
    for n in range(0, 10):
        print("sending LAUNCH")
        s.send(LAUNCH)
        sleep(0.05)

def land():
    for n in range(0, 10):
        print("sending LAND")
        s.send(LAND)
        sleep(0.05)

# Calculate UDP payload Checksum
def crunch(stuff):
    c = 0
    for x in stuff[1:]:
        c = c + x

    return chr((stuff[0] ^ c) % 256)


def display( str ):
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    #banner = font.render(banner, True, (255, 255, 255), (159, 182, 205))
    #bannerRect = banner.get_rect()
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    #bannerRect.centerx = screen.get_rect().centerx
    #bannerRect.centery += 100
    #screen.blit(banner, bannerRect)
    screen.blit(text, textRect)
    pygame.display.update()


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Drone Control')
screen.fill((159, 182, 205))

font = pygame.font.Font(None, 17)

done = False
flags = {"U": 0, "D": 0, "F": 0, "B": 0, "L": 0, "R": 0, "RL": 0, "RR": 0}
modes = "Place flight modes here"


#IPADDR = '172.16.10.1'
IPADDR = '127.0.0.1'
UDPPORTNUM = 8080
TCPPORTNUM = 8888

# UDP connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# TCP connection
t = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# connect the socket
s.connect((IPADDR, UDPPORTNUM))

start()
calibrate()

counter = 0
flying = False
SPEED = 0x00
while not done:

    # Base values for movement data
    UD = 0x7f
    LR = 0x3f
    FB = 0x3f
    ROT = 0x3f
    FBT = 0x00
    LRT = 0x00

    dispFlags = "SPEED:"+hex(SPEED)+" U:" + str(flags["U"]) + " D:" + str(flags["D"]) + " RL:" + str(flags["RL"]) + " RR:" + \
                str(flags["RR"]) + " F:" + str(flags["F"]) + " B:" + str(flags["B"]) + " L:" + str(flags["L"]) + \
                " R:" + str(flags["R"])

    display(dispFlags)
    pygame.event.pump()
    keys = pygame.key.get_pressed()


    if keys[Launch_key]:
        flying = True
        launcher()

    if keys[Land_key]:
        flying = False
        land()

    # land and exit
    if keys[Exit_key]:
        flying = False
        land()
        done = True
    # UP
    if keys[Up_key]:
        flags["U"] = 1
        UD += 0x30 + SPEED
    else:
        flags["U"] = 0

    # Down
    if keys[Down_Key]:
        flags["D"] = 1
        UD -= 0x30  + SPEED
    else:
        flags["D"] = 0

    # Rotate Left
    if keys[RotateL_key]:
        flags["RL"] = 1
        ROT -= 0x30 + SPEED
    else:
        flags["RL"] = 0

    # Rotate Right
    if keys[RotateR_key]:
        flags["RR"] = 1
        ROT += 0x30 + SPEED
    else:
        flags["RR"] = 0

    # Forward
    if keys[Forward_key]:
        flags["F"] = 1
        FB -= 0x20 + SPEED
    else:
        flags["F"] = 0

    # Backwards
    if keys[Back_key]:
        flags["B"] = 1
        FB += 0x20 + SPEED
    else:
        flags["B"] = 0

    # Left
    if keys[Left_key]:
        flags["L"] = 1
        LR -= 0x30 + SPEED
    else:
        flags["L"] = 0

    # Right
    if keys[Right_Key]:
        flags["R"] = 1
        LR += 0x30 + SPEED
    else:
        flags["R"] = 0
    # Trim
    if keys[F_trim_k]:
        flags["R"] = 1
        FBT -= 0x1
    if keys[B_trim_k]:
        flags["R"] = 1
        FBT += 0x1

    if keys[L_trim_k]:
        flags["R"] = 1
        LRT -= 0x1
    if keys[R_trim_k]:
        flags["R"] = 1
        LRT += 0x1

    if keys[Inc_speed_k] & (SPEED <= 0xC0):
        SPEED += 0x08
    if keys[Dec_speed_k] & (SPEED != 0x00):
        SPEED -= 0x08
    print(hex(SPEED +0x30))
    if flying:

        data = 0xff, 0x08, UD, ROT, FB, LR, 0x90, 0x10, 0x10, 0x02
        checksum = crunch(data)
        packet = ''.join(chr(x) for x in data) + checksum
        s.send(packet)

    # Send time every 20 iterations.
    if counter == 0:
        s.send(INIT)
        counter = 20
    counter -= 1

    sleep(.05)
