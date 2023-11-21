#!/usr/bin/env python3
import serial
import time
import sys
help = """
s Switch
l Listen
b Brighter
d Darker
"""

dev = "/dev/ttyS3"
frq = 9600

def to_hex_string(data):
    return ''.join('\\x{:02x}'.format(byte) for byte in data)

# use armbian-configure to turn on S3
if len(sys.argv)<1:
    print(help)
command = sys.argv[1]

if command=="s":
    # Switch
    with serial.Serial(dev, frq) as ser:
        # ser.write(b'\xfa\xF1\x00\xff\x01')
        ser.write(b'\xfa\xF1\x00\xff\x01')
elif command=="l":
    # Listen
    print("Receiving ...")
    with serial.Serial(dev, frq) as ser:
        while True:
            data = ser.read()
            print("Recv:", to_hex_string(data))
elif command=="b":
    with serial.Serial(dev, frq) as ser:
        ser.write(b'\xfa\xF1\x00\xff\x09')
elif command=="d":
    with serial.Serial(dev, frq) as ser:
        ser.write(b'\xfa\xF1\x00\xff\x11')
elif command=="bb":
    with serial.Serial(dev, frq) as ser:
        for _ in range(10):
            ser.write(b'\xfa\xF1\x00\xff\x09')
elif command=="dd":
    with serial.Serial(dev, frq) as ser:
        for _ in range(10):
            ser.write(b'\xfa\xF1\x00\xff\x11')
else:
    print(help)
