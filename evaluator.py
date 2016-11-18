# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 16:08:17 2016

@author: andsora
"""

import re
import sys

print("Here is Evalutor.")

class parser(object):
    def __init__(self, smassage):
        slist = smassage[2:-2].split(',')
        self.mode = slist[0]
        self.stype = slist[1]
        (self.src,self.dest) = slist[2].split('->')
        sizel = re.split("[()]", slist[3])
        self.size = float(sizel[0])
        self.txsize = float(sizel[1])
        self.seq = float(slist[4])
        self.cw = float(slist[5])
        self.cwsize = float(slist[6])
        self.dispatch = float(slist[7])
        self.stime = float(slist[8])
        
    def echo_self(self):
        print(self.mode)
        print(self.stype)
        print(self.src)
        print(self.dest)
        print(self.size)
        print(self.txsize)
        print(self.seq)
        print(self.cw)
        print(self.cwsize)
        print(self.dispatch)
        print(self.stime)

class evaluator():
    def __init__(self):
        self.count = 0
        self.totaltime = 0.0
        self.totalsize = 0.0
        self.waitqueue = {}
        
    def update(self, smassage):
        newparser = parser(smassage)
        if newparser.mode == 'T' and newparser.stype != 'A':
            self.waitqueue[newparser.seq] = newparser
        elif newparser.mode == 'R' and newparser.stype == 'A':
            oldparser = self.waitqueue.get(newparser.seq)
            if oldparser == None:
                print("Get a A, but Can't find a corresponding T!")
                sys.exit()
            self.count += 1
            self.totalsize += oldparser.size
            self.totaltime += newparser.stime - oldparser.stime
    
    def thrp(self):
        return self.totalsize / self.totaltime
        
    def delay(self):
        return self.totaltime / self.count