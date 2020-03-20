# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:38:26 2020

@author: Experimenter
"""

from psychopy import visual, event, monitors
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



mon1 = monitors.Monitor('whiteOLED_2_SADK_luma1200')  
mon2 = monitors.Monitor('whiteOLED_1_SADK_luma1200')


win1 = visual.Window(
        size = mon1.getSizePix(),
        monitor = mon1,
        winType = "pyglet",
        screen = 1,
        color = [-1, -1, -1],
        )
                         
win2 = visual.Window(
        size = mon2.getSizePix(),
        monitor = mon2,
        winType = "pyglet",
        screen = 0,
        color = [-1, -1, -1],
        )
 

line1 = visual.ShapeStim(win1)
line1.lineColor = 'white'
line1.units = "pix"

line2 = visual.ShapeStim(win2)
line2.lineColor = 'white'
line2.units = "pix"

v1,v2,v3 = square_coordinates(L = 200)

correction = np.array([10, 10])

corrected = False

for i in range(len(v1)):
    line1.vertices = [v1[i], v2[i]]
    line1.draw()    
    line2.vertices = [v1[i], v2[i]]
    line2.draw()

    

win1.flip()
win2.flip()

while True:
    
    key = event.waitKeys()
    
    if key[0] == "escape":
        break
    
    else:
        if corrected:            
            for i in range(len(v1)):
                line1.vertices = [v1[i], v2[i]]
                line1.draw()                
                line2.vertices = [v1[i], v2[i]]
                line2.pos = [0, 0]
                line2.draw()                              
        
            win1.flip()
            win2.flip()
            
            corrected = False
            
        else:
            for i in range(len(v1)):
                line1.vertices = [v1[i], v2[i]] 
                line1.draw()                
                line2.vertices = [v1[i], v2[i]]
                line2.pos += correction
                line2.draw()
                circ = visual.Circle(win1, units = "pix", edges = 128, radius = 5, fillColor = 'white')
                circ.draw()
        
            win1.flip()
            win2.flip()
            
            corrected = True

win1.close()
win2.close()