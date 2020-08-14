# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:03:41 2019

@author: Experimenter
"""


import traceback, collections, json, random, os, csv, pdb
import numpy as np
import pandas as pd
from psychopy import monitors, visual, event
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from tabulate import tabulate




def reflection_matrix():
    """ creates a matrix that reflects in the x = 0 axis"""
    reflect_mat = np.array([[-1, 0], [0, 1]])
    return reflect_mat


def rotation_matrix(theta):
    """ creates a rotation matrix to rotate throught angle theta """
    rotation_mat = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    return rotation_mat


def initialise_shapes(shape_parameters, run_type = 'test'):
    
    """ """
    
    if run_type == 'test':
        win = visual.Window(screen = 0,
                            color = shape_parameters['background_color'])
    
        """ Create lines to be presented on screens. Line vertices aranged here 
        as [[x1, x2, ..., xn], [y1, y2, y3, ..., yn]] to allow multiplication by 
        rotation matrix. For Psychopy, this needs to be transposed to become
        [[x1, y1], [x2,y2], ..., [xn, yn]]. """
        shape_vertices = np.array([ [-shape_parameters['line_length']/2, shape_parameters['line_length']/2], [0, 0] ])
        shape_position =  np.array([shape_parameters['line_length']/2 + shape_parameters['line_displacement'], shape_parameters['screen_position']])
        
        """ add values to shape parameters dictionary """
        shape_parameters['vertices'] = shape_vertices.tolist()
        shape_parameters['position'] = shape_position.tolist()
            
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
                monitor = mon1,
                winType = "pyglet",
                size = mon1.getSizePix(),
                screen = 0,
                color = shape_parameters['background_color'],
                )
#        win1.monitor = mon1
#        win1.size = mon1.getSizePix()
#        win1.winType = "pyglet"
#        win1.screen = 0
#        win1.color = shape_parameters['background_color']
#        try:
#            win1.monitor = mon1
#            win1.size = mon1.getSizePix()
#        except:
#            print('using default window size')

            
                 
        win2 = visual.Window(
                mointor = mon2,
                winType = "pyglet",
                size = mon2.getSizePix(),
                screen = 1,
                color = shape_parameters['background_color'],
                )
#        win2.winType = "pyglet"
#        win2.screen = 1
#        win2.color = shape_parameters['background_color']
#        try:
#            win2.size = mon2.getSizePix()
#            win2.monitor = mon2
#        except:
#            print('using default window size')
            
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


def update_shapes(shape1, shape2, shape_parameters, orientation = 0, offset = 0, run_type = 'test'):
    
    """ """
    
    
    rotate_mat = rotation_matrix(np.radians(orientation))
    reflect_mat = reflection_matrix()
    
    position = np.array(shape_parameters['position'])
    vertices = np.array(shape_parameters['vertices'])
    correction = np.array(shape_parameters['correction'])
    
    if run_type == 'test':
        
        shape1.pos = rotate_mat.dot(position).transpose()
        shape1.vertices = rotate_mat.dot(vertices).transpose()
        
        shape2.pos = rotate_mat.dot((np.array([-1, 1]) * position + np.array([0, offset]))).transpose()
        shape2.vertices = rotate_mat.dot(vertices).transpose()
        
    else:
        shape1.pos = rotate_mat.dot(position).transpose()
        shape1.vertices = rotate_mat.dot(vertices).transpose()

        shape2_shift = position + correction + np.array([0, offset])
        shape2.pos = reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(shape2_shift))).transpose()
        shape2.vertices = rotate_mat.dot(vertices).transpose()
    
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
    if row['key_choice'] in ['num_4', 'num_8', '4', '8','left','up']:
        return 1
    elif row['key_choice'] in ['num_2', 'num_6', '2', '6', 'right', 'down']:
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
        # pdb.set_trace()
        x_fit = np.linspace(min(x), max(x), 1000)
        ax.plot(x_fit, sigmoid(x_fit, *popt))
        return {'popt' : popt, 'pcov' : pcov}
    except Exception:
        traceback.print_exc()
        pass


def vernier_analysis(df, plot_title = 'title'):    
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

def offset_and_scale(orientations, fit_results, shape_parameters):
    R = [fit_results[orientation]['popt'][0] for orientation in orientations]
    
    x = R[0::2]
    y = R[1::2]
    
    width = max(x) - min(x)
    height = max(y) - min(y)
    
    shape_dim = shape_parameters['screen_position']
    
    width_ratio = (shape_dim + width)  / shape_dim
    height_ratio = (shape_dim + height) / shape_dim
    
    x0 = np.mean(x)
    y0 = np.mean(y)
    
    return width_ratio, height_ratio, x0, y0

def display_corrected(wins,x0,y0,dims = 500):
    rect1 = visual.Rect(
            wins[0],
            units = 'pix',
            width = dims,
            height = dims,
            )
    
    rect2 = visual.Rect(
            wins[1],
            units = 'pix',
            width = dims,
            height = dims,
            pos = (-x0, -y0),
            )
    
    return rect1, rect2
    
    
    
    


def save_data(filepath, alignment_data, fit_results, trial_parameters, shape_parameters):
    
    os.mkdir(filepath)

    alignment_data.to_csv(os.path.join(filepath,'alignment_data.csv'), sep = '\t')
    
    shape_parameters_file = os.path.join(filepath,'shape_parameters.csv')
    with open(shape_parameters_file, 'w') as f:
        w = csv.DictWriter(f, shape_parameters)
        w.writeheader()
        w.writerow(shape_parameters)
        
    trial_parameters_file = os.path.join(filepath,'trial_parameters.csv')
    with open(trial_parameters_file, 'w') as f:
        w = csv.DictWriter(f, trial_parameters)
        w.writeheader()
        w.writerow(trial_parameters)
        
    fit_results_file = os.path.join(filepath,'fit_results.csv')
    with open(fit_results_file, 'w') as f:
        w = csv.DictWriter(f, fit_results)
        w.writeheader()
        w.writerow(fit_results)

""" Trial class """
vernier_trial = collections.namedtuple('trial', ['orientation','offset'])


class vernier_trial_list:

    """ Trial List class """
    def __init__(self, orientations = np.array([0,90,180,270]), offsets = np.arange(-10,12,2), nreps = 1):
        self.orientations = orientations
        self.offsets = offsets
        self._trials = [vernier_trial(orientation, offset) 
                        for orientation in self.orientations 
                        for offset in self.offsets]*nreps
        
    def __len__(self):
        return len(self._trials)
    
    def __getitem__(self, position):
        return self._trials[position]
    
    def __setitem__(self, position, trial):
        self._trials[position] = trial
        
    def sort_by_offset(self):
        self._trials = sorted(self, key = lambda trial : trial.offset)
        
    def shuffle_trials(self):
        self.sort_by_offset()
        new_list = []
        new_trial_list = []
        self.sort_by_offset()
        for trial in self:
            dups = np.nonzero(new_list == trial.orientation)
            dups = np.concatenate([dups[0], dups[0] + 1])
            non_dups = np.setdiff1d(np.arange(0, len(new_list)+1), dups)
            new_pos = non_dups[random.randint(0, len(non_dups)-1)]
            new_list = np.insert(new_list, new_pos, trial.orientation)
            new_trial_list.insert(new_pos, vernier_trial(trial.orientation, trial.offset))
        self._trials = new_trial_list
    




# =============================================================================
# """ Test functions """
# 
# if __name__ == '__main__':
# 
#     run_type = 'test'
# 
#     """ Shape (line) parameters """
#     with open("default_shape_parameters.json","r") as read_file:
#         shape_parameters = json.load(read_file)
# 
# 
#     """ Trial parameters """ 
#     with open("default_trial_parameters.json","r") as read_file:
#         trial_parameters = json.load(read_file)
# 
# 
#     """ Build trial list class - # uses purpose-built 'vernier_trial_list' class"""
#     trial_list = vernier_trial_list(trial_parameters['orientations'],
#                                                 trial_parameters['offsets'],
#                                                 trial_parameters['nreps'],
#                                                 )
#     
#     trial_list.shuffle_trials() 
#     
#     trial_data = []
# 
# 
#     """ Initialise monitors, windows and shapes. A try/except/else structures 
#     should prevent a window being presented if there is an error in set-up (aiming
#     to avoid kernel death!) """
#     try:
#         wins, line1, line2, shape_parameters = initialise_shapes(shape_parameters, 
#                                                                  run_type)
# 
#     except Exception:
#         traceback.print_exc()
# 
#     else:
#         
#         """ Trial starts here """
#         try:
#             for trial in trial_list:
#                 line1, line2 = update_shapes(line1, 
#                                              line2, 
#                                              shape_parameters, 
#                                              trial.orientation, 
#                                              trial.offset, 
#                                              run_type)
#                 line1.draw()
#                 line2.draw()
#                 [win.flip() for win in wins]
#                 
#                 key_choice = event.waitKeys()                
# 
#                 
#                 if key_choice[0] == 'escape':
#                     break
#                 else:
#                     trial_data.append({'orientation' : trial.orientation,
#                                  'offset' : trial.offset,
#                                  'key_choice' : key_choice[0]
#                                  })
#                 
#                 df = pd.DataFrame(trial_data)
#                 fit_results = {}
#                 
#                 for orientation in trial_parameters['orientations']:
#                     fit_results[orientation] = vernier_analysis(
#                             df.sort_values('offset').loc[df['orientation'] == orientation], 
#                             plot_title = str(orientation),
#                             )
#                     
#                 table = tabulate_results(trial_parameters['orientations'], fit_results)
#                 
#         
#             """ End trial """
#             [win.close() for win in wins]
# 
#         
#         except Exception:
#             """ Close windows """
#             [win.close() for win in wins]
#             traceback.print_exc()
# =============================================================================
