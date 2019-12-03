# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:03:41 2019

@author: Experimenter
"""

import numpy as np
from psychopy import monitors, visual

reflect_mat = np.array([[-1, 0], [0, 1]])

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
    
#    shape1 = visual.ShapeStim(win,
#                             units = "pix",
#                             lineWidth = line_width,
#                             vertices = rotate_mat.dot(line_vertices).transpose(), # rotate by given angle, then transpose to suit psychopy input
#                             lineColor = [1, -1, -1],   # adust brightness (correct terminology? probs not)
##                             pos = rot_mat.dot(line_pos),
#                             )
#                             
#    shape2 = visual.ShapeStim(win,
#                             units = "pix",
#                             lineWidth = line_width,
#                             vertices = rotate_mat.dot(line_vertices).transpose(),
#                             lineColor = [-1, 1, -1],
##                             pos = rot_mat.dot(np.array([-1, 1]) * line_pos),
#                             )
    
    return (win, shape1, shape2)
    

def initialise_oleds(line_width, line_vertices, line_color, line_pos, rot_mat):
    """
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
                             vertices = rot_mat.dot(line_vertices).transpose(),
                             lineColor = line_color,   # adust brightness (correct terminology? probs not)
                             pos = rot_mat.dot(line_pos), # one of the screens is viewed backwards...
                             )
                             
    shape2 = visual.ShapeStim(win2,
                             units = "pix",
                             lineWidth = line_width,
                             vertices = reflect_mat.dot(rot_mat.dot(line_vertices)).transpose(),
                             lineColor = line_color,
                             pos = rot_mat.dot(np.array([-1, 1]) * line_pos),
                             )
    
    return (mon1, mon2, win1, win2, shape1, shape2)