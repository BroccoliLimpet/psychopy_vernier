# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:14:35 2019

@author: Experimenter
"""

from psychopy import visual, event
import numpy as np
import traceback


try:
    win = visual.Window()
    
    shape_vert = np.array([[-100, 100], [0, 0]])
    shape_pos = np.array([-(100 + 10), 0])
    
    theta = np.radians(45)
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    
    
    shape1 = visual.ShapeStim(win, 
                             units = "pix",
                             vertices = R.dot(shape_vert).transpose(),
                             pos = R.dot(shape_pos))
                             
    shape2 = visual.ShapeStim(win,
                              units = "pix",
                              vertices = R.dot(shape_vert).transpose(),
                              pos = R.dot(np.array([-1, 1]) * (shape_pos + np.array([0, 20]))))
                              
    shape1.draw()
    shape2.draw()
    
except Exception:
    traceback.print_exc()
    
    win.close()
    
else:    
    win.flip()
    
    event.waitKeys()
    
    win.close()
