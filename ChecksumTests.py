#!/usr/bin/env python
"""
This script was a testbed to establish how to calculated the needed checksum for the UDP command data.
The payload must be 11 bytes with [0] = 0xFF and the last byte being the checksum.

Methods that could be used:
    - Add all together then (~SUM-1)%256

    - Start at 0, subtract all add 1 and %256

    - Add all except for the 1st byte of 0xFF, XOR with 0xFF and %256

    All 3 give the same result.

    print(hex( 0xff^(0x08+0x7e+0x3f+0x40+0x3f+0x90+0x10+0x10+0x42)%256) )

    print(hex( (-0xff-0x08-0x7e-0x3f-0x40-0x3f-0x90-0x10-0x10-0x42-2)%256) )

    for x in a[1:]:
        c = c + x
    print(hex( (0xFF ^ c) % 256 ))

"""
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
            checksum = (byte + stuff[i])
        if (i > 1) & (i < len(stuff)):
            checksum = (checksum + stuff[i])
        i = i + 1




    print("-------- : checksum\n" + bin(checksum)[2:].zfill(num_of_bits) +" : "+ hex((~checksum -1)%256).upper() )
# Test methods
crunch(a)
crunch(b)

# Resulting method
def chksum(stuff):
    c = 0
    for x in stuff[1:]:
        c = c + x
    print(hex( (stuff[0] ^ c) % 256 ).upper())

chksum(a)
chksum(b)
