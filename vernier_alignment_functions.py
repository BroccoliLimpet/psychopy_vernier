# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:03:41 2019

@author: Experimenter
"""

import numpy as np
import pandas as pd
from psychopy import monitors, visual
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import config
#import pdb
import traceback
from tabulate import tabulate


def reflection_matrix():
    """ creates a matrix that reflects in the x = 0 axis"""
    reflect_mat = np.array([[-1, 0], [0, 1]])
    return reflect_mat


def rotation_matrix(theta):
    """ creates a rotation matrix to rotate throught angle theta """
    rotation_mat = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return rotation_mat


def initialise_shapes(shape_parameters, run_type = 'trial'):
    
    if run_type == 'test':
        win = visual.Window(screen = 2,
                            color = shape_parameters['background_color'])
    
        """ Create lines to be presented on screens. Line vertices aranged here 
        as [[x1, x2, ..., xn], [y1, y2, y3, ..., yn]] to allow multiplication by 
        rotation matrix. For Psychopy, this needs to be transposed to become
        [[x1, y1], [x2,y2], ..., [xn, yn]]. """
        shape_vertices = np.array([ [-shape_parameters['line_length']/2, shape_parameters['line_length']/2], [0, 0] ])
        shape_position =  np.array([shape_parameters['line_length']/2 + shape_parameters['line_displacement'], shape_parameters['screen_position']])
        
        """ add values to shape parameters dictionary """
        shape_parameters['vertices'] = shape_vertices
        shape_parameters['position'] = shape_position
            
        """ red line """
        shape_red = visual.ShapeStim(win, 
                                 units = "pix",
                                 vertices = shape_vertices.transpose(),
                                 pos = shape_position.transpose(),
                                 lineColor = [1, -1, -1], #shape_parameters['line_color'],
                                 )
            
        """ green line """                        
        shape_green = visual.ShapeStim(win,
                                  units = "pix",
                                  vertices = shape_vertices.transpose(),
                                  pos = shape_position.transpose(), # pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(shape_position))).transpose(),
                                  lineColor = [-1, 1, -1], #shape_parameters['line_color'],
                                  )
        
        return ([win], shape_red, shape_green, shape_parameters)
    
    
    else:
        """ One set of coordinates is used for both lines, but the position of 
        line 2 is the relfection in the y-axis. Screen 2 is seen as a reflection #
        of itself, due to the reflection at the beam splitter. To counteract this, 
        the line is reflected in the y-axis for a second time."""
            
        """ Create lines to be presented on screens. Line vertices aranged here 
        as [[x1, x2, ..., xn], [y1, y2, y3, ..., yn]] to allow multiplication by 
        rotation matrix. For Psychopy, this needs to be transposed to become
        [[x1, y1], [x2,y2], ..., [xn, yn]]. """
        shape_vertices = np.array([ [-shape_parameters['line_length']/2, shape_parameters['line_length']/2], [0, 0] ])
        shape_position =  np.array([shape_parameters['line_length']/2 + shape_parameters['line_displacement'], shape_parameters['screen_position']])
        
        """ add values to shape parameters dictionary """
        shape_parameters['vertices'] = shape_vertices
        shape_parameters['position'] = shape_position
        
        
        """ Gain access to calibration/screen information """
        mon1 = monitors.Monitor('whiteOLED_2_SADK_luma1200')  
        mon2 = monitors.Monitor('whiteOLED_1_SADK_luma1200')  
        
        """ Initialise windows  """
        win1 = visual.Window(
                size = mon1.getSizePix(),
                monitor = mon1,
                winType = "pyglet",
                screen = 0,
                color = shape_parameters['background_color'],
                )
                         
        win2 = visual.Window(
                size = mon2.getSizePix(),
                monitor = mon2,
                winType = "pyglet",
                screen = 1,
                color = shape_parameters['background_color'],
                )
        
        wins = [win1, win2]
        
        """ Create shapes to be presented on screens """
        shape1 = visual.ShapeStim(win1,
                                 units = "pix",
                                 lineWidth = shape_parameters['line_width'],
                                 vertices = shape_vertices.transpose(),
                                 lineColor = shape_parameters['line_color'],   # adust brightness (correct terminology? probs not)
                                 pos = shape_position.transpose(), 
                                 )
                                 
        shape2 = visual.ShapeStim(win2,
                                 units = "pix",
                                 lineWidth = shape_parameters['line_width'],
                                 vertices = shape_vertices.transpose(),
                                 lineColor = shape_parameters['line_color'],
                                 pos = shape_position.transpose(),
                                 )
        
        return wins, shape1, shape2, shape_parameters


def update_shapes(shape1, shape2, shape_parameters, orientation = 0, offset = 0, run_type = 'trial'):
    rotate_mat = rotation_matrix(np.radians(orientation))
    reflect_mat = config.reflect_mat
    
    if run_type == 'test':
        shape1.pos = rotate_mat.dot(shape_parameters['position']).transpose()
        shape1.vertices = rotate_mat.dot(shape_parameters['vertices']).transpose()
        shape2.pos = rotate_mat.dot(shape_parameters['position'] + np.array([0, offset])).transpose() + shape_parameters['correction']
        shape2.vertices = rotate_mat.dot(shape_parameters['vertices']).transpose()
        
    else:
        shape1.pos = rotate_mat.dot(shape_parameters['position']).transpose()
        shape1.vertices = rotate_mat.dot(shape_parameters['vertices']).transpose()
        shape2_shift = shape_parameters['position'] + np.array([0, offset])
        shape2.pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(shape2_shift))).transpose() + shape_parameters['correction']
#        shape2.pos = rotate_mat.dot(shape2_shift).transpose()
        shape2.vertices = rotate_mat.dot(shape_parameters['vertices']).transpose()
    
    return shape1, shape2


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
    return df, file_path


def choice_to_value(row):
    if row['key_choice'] in ['num_4', 'num_8']:
        return 1
    elif row['key_choice'] in ['num_2', 'num_6']:
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


def vernier_fit(x,y,p0,ax):
    try:
        popt, pcov = curve_fit(sigmoid, x, y, p0)
        x_fit = np.linspace(min(x), max(x), 1e3)
        ax.plot(x_fit, sigmoid(x_fit, *popt))
        return {'popt' : popt, 'pcov' : pcov}
    except Exception:
        traceback.print_exc()


def vernier_analysis(df, plot_title):    
    df['choice_bin'] = df.apply(lambda row: choice_to_value(row), axis = 1)
    fig, ax = plt.subplots()
    df.groupby(['offset']).mean().plot(y = 'choice_bin', marker = 'o', linestyle = '', ax = ax)
    ax.legend().set_visible(False)
    ax.set_title(plot_title)
    fit_results = vernier_fit(df.offset, df.choice_bin, (10,0), ax)
    return fit_results

def tabulate_results(orientations, fit_results):
    orientations.sort()
    table = []
    for orientation in orientations:
        table.append([orientation, fit_results[orientation]['popt'][0]])
    print(tabulate(table, headers = ["Orientation", "Offset"]))
    return table
    
