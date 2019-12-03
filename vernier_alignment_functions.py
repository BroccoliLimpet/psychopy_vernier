# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:03:41 2019

@author: Experimenter
"""

import numpy as np
from psychopy import monitors, visual
import constant

reflect_mat = constant.reflect_mat

def rotation_matrix(theta):
    """
    """
#    theta = np.radians(input("Enter orientation in degrees: "))
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return R
    

def initialise_test(line_width, line_vertices, line_pos, rotate_mat):
  
    win = visual.Window()
    
    # Create lines to be presented on screens
    
    """ red line """
    shape1 = visual.ShapeStim(win, 
                             units = "pix",
                             vertices = rotate_mat.dot(line_vertices).transpose(),
                             pos = rotate_mat.dot(line_pos).transpose(),
                             lineColor = [1, -1, -1],
                             )
        
    """ green line """                        
    shape2 = visual.ShapeStim(win,
                              units = "pix",
                              vertices = reflect_mat.dot(rotate_mat.dot(line_vertices)).transpose(),
                              pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(line_pos))).transpose(),
                              lineColor = [-1, 1, -1],
                              )    
    
   
    return (win, shape1, shape2)
    

def initialise_oleds(line_width, line_vertices, line_color, line_pos, rotate_mat):
    """
    One set of coordinates is used for both lines, but the position of line 2
    is the relfection in the y-axis.
    
    Screen 2 is seen as a reflection of itself, due to the reflection at the 
    beam splitter. To counteract this, the line is reflected in the y-axis for 
    a second time.
    """
        
    
    # Gain access to calibration/screen information
    mon1 = monitors.Monitor('whiteOLED_2_SADK_luma1200')  
    mon2 = monitors.Monitor('whiteOLED_1_SADK_luma1200')  
    
    # Initialise windows  
    win1 = visual.Window(size = mon1.getSizePix(),
                        monitor = mon1,
                        winType = "pyglet",
                        screen = 1,
                        color = [0.2, 0.2, 0.2])
                     
    win2 = visual.Window(size = mon2.getSizePix(),
                        monitor = mon2,
                        winType = "pyglet",
                        screen = 2,
                        color = [1, 1, 1])
      
    
    # Create lines to be presented on screens
    shape1 = visual.ShapeStim(win1,
                             units = "pix",
                             lineWidth = line_width,
                             vertices = rotate_mat.dot(line_vertices).transpose(),
                             lineColor = line_color,   # adust brightness (correct terminology? probs not)
                             pos = rotate_mat.dot(line_pos).transpose(), 
                             )
                             
    shape2 = visual.ShapeStim(win2,
                             units = "pix",
                             lineWidth = line_width,
                             vertices = reflect_mat.dot(rotate_mat.dot(line_vertices)).transpose(),
                             lineColor = line_color,
                             pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(line_pos))).transpose(),
                             )
    
    return (mon1, mon2, win1, win2, shape1, shape2)