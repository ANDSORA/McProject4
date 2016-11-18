# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:07:17 2016

@author: andsora
"""

import serial
import time
import threading
import parse
import json
import getopt


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
                    parse.parse(content)


class VlcSender(threading.Thread):
    def __init__(self, ser, destination):
        threading.Thread.__init__(self)
        self.s = ser
        self.d = destination

    def run(self):
        while True:
            line = input()
            print(line)
            s.write(("m["+line+"\0,"+self.d+"]\n").encode("ascii"))
            time.sleep(0.2)


getopt.getopt()
config = json.load(open("config.JSON"))
s = serial.Serial(config["path"], 115200, timeout=1)  # opens a serial port (resets the device!)
time.sleep(2)  # give the device some time to startup (2 seconds)

# write to the device’s serial port
s.write(("a["+config["address"]+"]\n").encode("ascii"))  # set the device address to AB
time.sleep(0.1)  # wait for settings to be applied

s.write(b"c[1,0,5]\n")  # set number of retransmissions to 5
time.sleep(0.1)  # wait for settings to be applied

s.write(b"c[0,1,30]\n")  # set FEC threshold to 30 (apply FEC to packets with payload >= 30)
time.sleep(0.1)  # wait for settings to be applied

receiver_thread = VlcReceiver(s)
sender_thread = VlcSender(s, config["destination"])

sender_thread.start()
receiver_thread.start()

sender_thread.join()
receiver_thread.join()

