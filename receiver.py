__author__ = 'liuyang'

import threading.Thread
import serial


class VLCReceiver(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__()
        self.s = ser

    def run(self):
        while True:
            print(self.s.readline())


