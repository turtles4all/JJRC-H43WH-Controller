#!/usr/bin/env python

#               U/D   ROT   F/B    L/R  CMD                      Checksum
a = 0xff, 0x08, 0x7e, 0x3f, 0x40, 0x3f, 0x90, 0x10, 0x10, 0x00 # 0x0b
b = 0xff, 0x08, 0x7e, 0x3f, 0x40, 0x3f, 0x90, 0x10, 0x10, 0x42 # 0xc9

def crunch(stuff):
    num_of_bits = 8
    i = 1
    checksum = 0
    for byte in stuff:

        print( (bin(byte))[2:].zfill(num_of_bits) + " : " + hex(byte).upper().zfill(2) + " : " + (bin(checksum))[2:].zfill(num_of_bits) )
        if i == 1:
            checksum = (byte ^ stuff[i])
        if (i > 1) & (i < len(stuff)):
            checksum = (checksum ^ stuff[i])
        i = i + 1




    print("-------- : checksum\n" + bin(checksum)[2:].zfill(num_of_bits) +" : "+ hex(checksum).upper() )
    print(checksum)
    
crunch(a)
print(" ")
crunch(b)
