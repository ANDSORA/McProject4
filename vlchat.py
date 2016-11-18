# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:07:17 2016

@author: andsora
"""

import serial
#import sys
import time
import evaluator

print("Here is VLchat!")
#open the Arouino
"""
while True:
    try:
        Sername = input("tell me your name: ")
        Ser = serial.Serial(Sername, 115200, timeout = 1)
        break
    except:
        print("Ooops, invalid serial portname!")"""
#give Arouino some time to init itself
Ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)
time.sleep(2)

#configure the Arouino
"""Addr = input("give the address: ")
Ser.write(("a[" + Addr + "]\n").encode("ascii"))"""
Ser.write(b"a[AB]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))

Ser.write(b"c[1,0,5]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))

Ser.write(b"c[0,1,30]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))

