#!/usr/bin/env python
# encoding: utf-8
"""
test.py
Created by Jerry on 2011-07-18.
"""

import sys
import os
import random

from pyheatmap import ReadClicks, Heatmap

def main():
    data = []
    for i in range(0, 3000):
        dot = "%s,%s" % (random.randint(0,800), random.randint(0,2000))
        data.append(dot)
    
    log_data = ReadClicks(data, 500)
    heatmap = Heatmap(log_data.coords, 'tmp/tmp')
    print "Heatmap saved: ", heatmap.make()
    
if __name__ == '__main__':
    main()