#!/usr/bin/env python

import socket
from time import sleep

# The IP of the quadcopter plus the UDP port it listens to for control commands
#IPADDR = '172.16.10.1'
IPADDR = '127.0.0.1'
UDPPORTNUM = 8080
TCPPORTNUM = 8888

INIT = '26e207000002000000030000000600000015000000070000002c000000'.decode('hex')
START = 'ff08003f403f1010100009'.decode('hex') 

ARM = 'ff087e3f403f9010100209'.decode('hex')
CAL = 'ff087e3f403fd0101002c9'.decode('hex')
SPINUP = 'ff087e3f403f90101042c9'.decode('hex')
LAUNCH = 'ff08f830403f901010029e'.decode('hex')
LAND = 'ff087e3f403f9010108289'.decode('hex')

START_KEY  = 'A'
CAL_KEY    = 'C'
SPIN_KEY   = 'S'
LAUNCH_KEY = 'PAGE UP'
LAND_KEY   = 'PAGE DOWN'

# coding=utf-8

# imports the Pygame library
import pygame


def main():
    # initializes Pygame
    pygame.init()

    # sets the window title
    pygame.display.set_caption(u'Keyboard events')

    # sets the window size
    pygame.display.set_mode((100, 100))
    SEND = 0
    # infinite loop
    pygame.key.set_repeat(50, 50)
    while True:
        # gets a single event from the event queue
        event = pygame.event.poll()

	    # captures the 'KEYDOWN' and 'KEYUP' events
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
	        # gets the key name
	        key_name = pygame.key.name(event.key)

	        # converts to uppercase the key name
	        key_name = key_name.upper()

	        # if any key is pressed
	        if event.type == pygame.KEYDOWN:
	            # prints on the console the key pressed
	            #print u'"{}" key pressed'.format(key_name)
				if key_name == START_KEY:
					print("START")
					SEND = 1
					s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
					t = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
					s.connect((IPADDR, UDPPORTNUM))
					for n in range(0,10): 
						print("sending INIT")
						s.send(INIT)
						sleep(0.05) 
					t.connect((IPADDR, TCPPORTNUM))
					CMD = ARM

				if key_name == CAL_KEY:
					print("CAL")
					for n in range(0,5): 
						print("sending Calibrate")
						s.send(CAL)
						sleep(0.05)
					sleep(2)

				if key_name == SPIN_KEY:
					print("SPINUP")
					CMD = SPINUP

				if key_name == LAUNCH_KEY:
					print("LAUNCH")
					CMD = LAUNCH

				if key_name == LAND_KEY:
					print("LAND")
					CMD = LAND

				if key_name == 'Q':
					print("E-STOP")
					for n in range(0,5): 
						print("sending LAND")
						s.send(LAND)
						sleep(0.02)
					t.close()
					s.close()
					pygame.quit()
                    
	
		if SEND == 1:
			s.send(CMD)
	        # if any key is released
	        #elif event.type == pygame.KEYUP:
	            # prints on the console the released key
	         #   print u'"{}" key released'.format(key_name)
	
		

    # finalizes Pygame
    pygame.quit()


if __name__ == '__main__':
    main()
