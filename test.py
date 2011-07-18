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
    for i in range(0, 1000):
        dot = "%s,%s" % (random.randint(0,800), random.randint(0,2000))
        data.append(dot)
    
    print data
        
    log_data = ReadClicks(data)
    heatmap = Heatmap(log_data.coords, 'tmp/tmp')
    heatmap.normalizespot()
    heatmap.iterate()
    heatmap.colorize()

if __name__ == '__main__':
    main()