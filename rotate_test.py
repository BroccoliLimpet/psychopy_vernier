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
    shape_pos = np.array([[100], [0]])
    
    theta = np.radians(90)
    rotate_mat = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    
    reflect_mat = np.array([[-1, 0], [0, 1]])
    
    """ red line """
    shape1 = visual.ShapeStim(win, 
                             units = "pix",
                             vertices = rotate_mat.dot(shape_vert).transpose(),
                             pos = rotate_mat.dot(shape_pos).transpose(),
                             lineColor = [1, -1, -1],
                             )
    
    """ green line """                        
    shape2 = visual.ShapeStim(win,
                              units = "pix",
                              vertices = reflect_mat.dot(rotate_mat.dot(shape_vert)).transpose(),
                              pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(shape_pos))).transpose(),
                              lineColor = [-1, 1, -1],
                              )
                              
    shape1.draw()
    shape2.draw()
    
except Exception:
    traceback.print_exc()
    
    win.close()
    
else:    
    win.flip()
    
    event.waitKeys()
    
    win.close()
