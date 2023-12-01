#!/usr/bin/env python3
import serial
import time
import sys
import time
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

def switch():
    with serial.Serial(dev, frq) as ser:
        # ser.write(b'\xfa\xF1\x00\xff\x01')
        ser.write(b'\xfa\xF1\x00\xff\x01')
def listen():
    with serial.Serial(dev, frq) as ser:
        while True:
            data = ser.read()
            print("Recv:", to_hex_string(data))

def brighter(l:int=1):
    with serial.Serial(dev, frq) as ser:
        for _ in range(l):
            ser.write(b'\xfa\x50\x00\xff\x09')
            time.sleep(0.3)

def darker(l:int=1):
    with serial.Serial(dev, frq) as ser:
        for _ in range(l):
            ser.write(b'\xfa\x50\x00\xff\x11')
            time.sleep(0.3)

def bb():
    with serial.Serial(dev, frq) as ser:
        for _ in range(5):
            ser.write(b'\xfa\x9F\x00\xff\x09')
            time.sleep(0.3)
def dd():
    with serial.Serial(dev, frq) as ser:
        for _ in range(5):
            ser.write(b'\xfa\x9F\x00\xff\x11')
            time.sleep(0.3)

if __name__ == "__main__":
    # use armbian-configure to turn on S3
    if len(sys.argv)<1:
        print(help)
    command = sys.argv[1]

    if command=="s":
        # Switch
        switch()
    elif command=="l":
        # Listen
        print("Receiving ...")
        listen()
    elif command=="b":
        brighter()
    elif command=="d":
        darker()
    elif command=="bb":
        bb()
    elif command=="dd":
        dd()
    else:
        print(help)
