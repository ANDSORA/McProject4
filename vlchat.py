# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:07:17 2016

@author: andsora
"""

import serial
import time
import threading
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
        print("Ooops, invalid serial portname!")
#give Arouino some time to init itself
Ser = serial.Serial("/dev/ttyACM0", 115200, timeout = 1)
time.sleep(2)"""

#configure the Arouino
"""Addr = input("give the address: ")
Ser.write(("a[" + Addr + "]\n").encode("ascii"))
Ser.write(b"a[AB]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))

Ser.write(b"c[1,0,5]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))

Ser.write(b"c[0,1,30]\n")
time.sleep(0.1)
print(Ser.readline().decode("utf-8"))"""

myeval = evaluator()

class VlcReceiver(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.s = ser

    def run(self):
        while True:
            received = self.s.readline().decode('unicode_escape').strip()
            if len(received) > 0:
                event_type = received[0]
                content = received[2:-1]
                if event_type == 'm':
                    print(content)
                elif event_type == "s":
                    myeval.update(content)


class VlcSender(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.s = ser

    def run(self):
        while True:
            line = input()
            print(line)
            s.write(("m["+line+"\0,AB]\n").encode("ascii"))
            time.sleep(0.2)


s = serial.Serial('/dev/tty.usbmodem1411', 115200, timeout=1)  # opens a serial port (resets the device!)
time.sleep(2)  # give the device some time to startup (2 seconds)

# write to the device’s serial port
s.write(b"a[CD]\n")  # set the device address to AB
time.sleep(0.1)  # wait for settings to be applied

s.write(b"c[1,0,5]\n")  # set number of retransmissions to 5
time.sleep(0.1)  # wait for settings to be applied

s.write(b"c[0,1,30]\n")  # set FEC threshold to 30 (apply FEC to packets with payload >= 30)
time.sleep(0.1)  # wait for settings to be applied

# s.write(b"m[hello world!\0,AB]\n")  # send message to device with address CD

sender_thread = VlcReceiver(s)
sender_thread.start()

receiver_thread = VlcSender(s)
receiver_thread.start()

sender_thread.join()
receiver_thread.join()

