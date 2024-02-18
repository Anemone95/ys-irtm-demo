#!/usr/bin/env python3
import serial

dev="/dev/ttyS4"
frq=9600

def getCo2():
    with serial.Serial(dev, frq) as ser:
        l=ser.read(6)
        if l[5] == (l[0]+l[1]+l[2]+l[3]+l[4])%256:
            return l[1]*256+l[2]
        else:
            return -1 

