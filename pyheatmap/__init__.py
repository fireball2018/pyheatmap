#!/usr/bin/env python
# encoding: utf-8
from __future__ import division

"""
__init__.py
Created by Jerry on 2011-07-18.
"""

import sys
import os
import random
import math

class Point():

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return "x%sy%s" % (self.x, self.y)

class ClickLog():

    x = 0
    y = 0
    items = []
    reps = 0

    def __init__(self, x, y, items):

        self.x = x
        self.y = y
        self.items = items

        points = {}

        for item in items:
            if item.xy in points:
                points[item.xy] += 1
            else:
                points[item.xy] = 1

        if len(points) > 0:
            self.reps = points[max(points)]

class ReadClicks():

    data = []

    def __init__(self, data, select_dots=1000):
        
        select_dots = select_dots > 10 and round(select_dots + select_dots*0.1) or select_dots
        
        if len(data) > select_dots:
            new_data = []

            for i in range(0, select_dots):
                new_data.append(random.choice(data))

            data = new_data
            del new_data

        for dot in data:

            dot = dot.split(",")

            if len(dot) >= 2 and dot[0].isdigit() and dot[1].isdigit():
                self.data.append(Point(int(dot[0]), int(dot[1])))

    @property
    def coords(self):

        if type(self.data) is not list and len(self.data) <= 0:
            return None

        max_x = 0
        max_y = 0

        coords = []

        for dot in self.data:
            coords.append(dot)
            max_x = dot.x > max_x and dot.x or max_x
            max_y = dot.y > max_y and dot.y or max_y

        return ClickLog(max_x, max_y, coords)

class Heatmap():

    dotimage    = 'bolilla.png'
    colorimage  = 'colors.png'
    opacity     = 0.5
    dotwidth    = 64
    format      = 'png'
    data        = None
    name        = ''
    
    def __init__(self, data, name):
        """docstring for __init__"""
        
        self.data = data
        self.name = name
        
        res_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "res")
        self.dotimage = os.path.join(res_dir, "bolilla.png")
        self.colorimage = os.path.join(res_dir, "colors.png")

    def normalizespot(self):
        """docstring for normalizespot"""
        intensity = 100-math.ceil(100/self.data.reps)
        normalize = 'convert "%s" -fill white -colorize %s%% %s.bol.png' % (self.dotimage, intensity, self.name)
        
        os.system(normalize)
        
    def iterate(self):
        """docstring for iterate"""
        halfwidth = self.dotwidth/2
        compose = []
        compose.append("convert -page %sx%s pattern:gray100" % (self.data.x + halfwidth, self.data.y + halfwidth))

        for dot in self.data.items:
            
            dot_x = dot.x - halfwidth
            dot_y = dot.y - halfwidth
            
            if dot_x >= 0 and dot_y  >= 0:
                compose.append("-page +%s+%s %s.bol.png" % (dot_x, dot_y, self.name))
            
        compose.append("-background white -compose multiply -flatten %s.empty.png" % self.name)
        compose = " ".join(compose)
        
        os.system(compose)
        
    def colorize(self):
        """docstring for colorize"""
        
        #invert image...
        invert = "convert %(name)s.empty.png -negate %(name)s.full.png" % {'name':self.name};
        os.system(invert)

        #colorize it...
        colorize = 'convert %(name)s.full.png -type TruecolorMatte %(colorimage)s -fx "v.p{0,u*v.h}" %(name)s.colorized.png' % {'name':self.name, 'colorimage':self.colorimage};
        os.system(colorize)
        
        #and apply transparency...
        transparency = 'convert %(name)s.colorized.png -channel A -fx "A*%(opacity)s" %(name)s.final.%(format)s' % {'name':self.name, 'opacity':self.opacity, 'format':self.format}
        os.system(transparency)
    
    def make(self):
        """docstring for make"""
        self.normalizespot()
        self.iterate()
        self.colorize()
        
        return "%(name)s.final.%(format)s" % {'name':self.name, 'format':self.format}