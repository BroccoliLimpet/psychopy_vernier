# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:03:13 2020

@author: Experimenter
"""

from psychopy import visual, event
import numpy as np



def condition1(x,y):
    return abs(x) != abs(y)

def condition2(x,y):
    return ((abs(x) == abs(y)) and ((x and y) != 0))

def square_coordinates(L = 100):
    
    coords = L * np.array([-1, 0, 1])
    
    v1 = np.array([ [x,y] for x in coords for y in coords if condition1(x,y)])
    
    v2 = np.array([ [x,y] for x in coords for y in -1*coords if condition2(x,y)])
    
    v3 = v2 * np.array([[1,-1], [-1,1], [-1,1], [1,-1]])
    
    return v1, v2, v3


win1 = visual.Window(screen = 2)
win2 = visual.Window(screen = 3)

line1 = visual.ShapeStim(win1)
line1.lineColor = 'white'
line1.units = "pix"

line2 = visual.ShapeStim(win2)
line2.lineColor = 'white'
line2.units = "pix"

v1,v2,v3 = square_coordinates()

for i in range(len(v1)):
    line1.vertices = [v1[i], v2[i]]
    line1.draw()
    
    line2.vertices = [v3[i], v1[i]]
    line2.draw()

win1.flip()
win2.flip()

event.waitKeys()

win1.close()
win2.close()