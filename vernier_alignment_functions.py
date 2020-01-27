# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:03:41 2019

@author: Experimenter
"""

import constant
import numpy as np
import pandas as pd
from psychopy import monitors, visual
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


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
    



def initialise_oleds(line_width, line_vertices, line_color, line_pos, rotate_mat, background_color):
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
#                        color = [0.2, 0.2, 0.2],
                        color = background_color,
                        )
                     
    win2 = visual.Window(size = mon2.getSizePix(),
                        monitor = mon2,
                        winType = "pyglet",
                        screen = 2,
                        color = background_color,
                        )
      
    
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




def csv_to_dataframe_filepath(file_path, **kwargs):
    # read file in as data frame
    df = pd.read_csv(file_path, sep = "\t")
    
    # if sort argument passed in, sort dataframe on the value given
    if kwargs:
        df = df.sort_values(kwargs["sort"])
    
    # return the dataframe
    return df



def csv_to_dataframe_gui(**kwargs):
    # user finds file through GUI
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile()
    
    # read file in as data frame
    df = pd.read_csv(file_path, sep = "\t")
    
    # if sort argument passed in, sort dataframe on the value given
    if kwargs:
        df = df.sort_values(kwargs["sort"])
    
    # return the dataframe
    return df

def choice_to_value(row):
    if row['choice'] in ['num_1', 'num_4', 'num_7'] or row['choice'] in ['num_7', 'num_8', 'num_9']:
        return 1
    elif row['choice'] in ['num1', 'num_2', 'num_3'] or row['choice'] in ['num_3', 'num_6', 'num_9']:
        return 0
    
def vernier_plot(df, **kwargs):
    fig, ax = plt.subplots()   
    df['choice_bin'] = df.apply(lambda row: choice_to_value(row), axis = 1)
    df.groupby(['offset']).mean().plot(y = 'choice_bin', marker = 'o', linestyle = '', ax = ax)
    ax.legend().set_visible(False)
    if kwargs:
        ax.xaxis.set_ticks(kwargs['ticks'])
    return fig, ax


def sigmoid(x, x0, k):
    y = 1 / (1 + np.exp(-k*(x-x0)))
    return y

def vernier_fit(x,y,ax):
#    plt.plot(x,y)
    popt, copt = curve_fit(sigmoid, x, y)
    x_fit = np.linspace(min(x), max(x), 1e3)
    ax.plot(x_fit, sigmoid(x_fit, *popt))
    return popt, copt

