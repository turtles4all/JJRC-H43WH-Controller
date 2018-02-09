"""
Controls:
	W/A/S/D - Up, Down, Rotate Left, Rotate Right

	arrow keys: 
	Up/Down/Left/Right - Forward, Bacwards, Left, Right
	Commands / Modes
	E-Stop - ESC

"""
import pygame
from pygame.locals import *
from time import sleep


# Calculate UDP payload Checksum
def chksum(stuff):
    c = 0
    for x in stuff[1:]:
        c = c + x
    return ((stuff[0] ^ c) % 256)


def display(banner, str):
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    banner = font.render(banner, True, (255, 255, 255), (159, 182, 205))
    bannerRect = banner.get_rect()
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery
    bannerRect.centerx = screen.get_rect().centerx
    bannerRect.centery += 100
    screen.blit(banner, bannerRect)
    screen.blit(text, textRect)
    pygame.display.update()


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Drone Control')
screen.fill((159, 182, 205))

font = pygame.font.Font(None, 17)

done = False
flags = {"U": 0, "D": 0, "F": 0, "B": 0, "L": 0, "R": 0, "RL": 0, "RR": 0}

while not done:
    # Base values for movment data
    UD = 0x7f
    LR = 0x3f
    FB = 0x3f
    ROT = 0x3f
    banner = "Place flight modes here"
    dispFlags = " U:" + str(flags["U"]) + " D:" + str(flags["D"]) + " RL:" + str(flags["RL"]) + " RR:" + \
                str(flags["RR"]) + " F:" + str(flags["F"]) + " B:" + str(flags["B"]) + " L:" + str(flags["L"]) + \
                " R:" + str(flags["R"])
    
    display(banner, dispFlags)

    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        done = True
    # UP
    if keys[K_w]:
        flags["U"] = 1
        UD += 0x10
    else:
        flags["U"] = 0

    # Down
    if keys[K_s]:
        flags["D"] = 1
        UD -= 0x10
    else:
        flags["D"] = 0

    # Rotate Left
    if keys[K_a]:
        flags["RL"] = 1
        ROT -= 0x10
    else:
        flags["RL"] = 0

    # Rotate Right
    if keys[K_d]:
        flags["RR"] = 1
        ROT += 0x10
    else:
        flags["RR"] = 0

    # Forward
    if keys[K_UP]:
        flags["F"] = 1
        FB += 0x10

    else:
        flags["F"] = 0

    # Backwards
    if keys[K_DOWN]:
        flags["B"] = 1
        FB -= 0x10
    else:
        flags["B"] = 0

    # Left
    if keys[K_LEFT]:
        flags["L"] = 1
        LR -= 0x10
    else:
        flags["L"] = 0

    # Right
    if keys[K_RIGHT]:
        flags["R"] = 1
        LR += 0x10
    else:
        flags["R"] = 0

    packet = [0xff, 0x08, UD, ROT, FB, LR, 0x90, 0x10, 0x10, 0x42]
    chk = chksum(packet)
    packet.append(chk)
    print(packet)
    sleep(.05)
