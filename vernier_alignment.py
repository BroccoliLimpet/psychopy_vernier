# -*- coding: utf-8 -*-
"""
Script to present horizontal (or vertical) lines to a subject.

Aim is that each line is presented on a different OLED monitor. Each monitor is
optically filtered - one appears green, the other red

Subject uses keyboard to indicate whether green line is above or below red 
line.

Created on Thu Nov 21 15:13:17 2019

@author: Tom Smart
"""


import numpy as np
from psychopy import data, visual, event, monitors
import traceback
import vernier_alignment_functions as funs


theta, rot_mat = funs.rotation_matrix()


## VARIABLES ##

""" The position of the two lines changes between each trial. 
Parameters set here."""
 
# minimum central position of line pair
min_pos = -20
# maximum central position of line pair  
max_pos = 20    

""" The offset between the two lines change between each trial.
Paraameter set here. """

# largest negative offset (i.e. green below red)
offset_low = -10   
# largest positive offset
offset_high = 10   
# offset increment
offset_step_size = 2  
# generate array of possible offset values
offsets = np.arange(offset_low, 
                    offset_high + offset_step_size, 
                    offset_step_size)   

""" The number of trials and possible subject keyboard inputs"""

# trial repeats
n_reps = 1  
# possible keyboard entries
key_list = ['num_1', 'num_2', 'num_3', 'num_7', 'num_8', 'num_9', 'escape']   


""" Line parameters """

line_width = 5
line_length = 300   
# separation of line ends
line_displacement = 25  
line_color = [-1, -1, -1]

""" Line vertices aranged here as [[x1, x2, ..., xn], [y1, y2, y3, ..., yn]] to 
allow multiplication  by rotation matrix. For Psychopy, this needs to be 
arranged as [[x1, y1], [x2,y2], ..., [xn, yn]]. """

line_vertices = np.transpose(rot_mat.dot(np.array([[-line_length/2, line_length/2], [0, 0]])))
line_pos = np.transpose(rot_mat.dot((line_length/2 + line_displacement, 0)))

""" Initialise trial data dictionary and list of dictionaries """
trial = {}  # initialise trial parameters dictionary
trial_list = [] # initialise list of dictionaries




# try/except to prevent window being presented if there is an error in set-up
try:
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
                             vertices = line_vertices,
                             lineColor = line_color,   # adust brightness (correct terminology? probs not)
                             pos = line_pos, # one of the screens is viewed backwards...88
                             )
                             
    shape2 = visual.ShapeStim(win2,
                             units = "pix",
                             lineWidth = line_width,
                             vertices = line_vertices,
                             lineColor = line_color,
                             pos = line_pos,
                             )
                             
    # build trial parameter dictionaries for psychopy's 'TrialHandler'
    for offset in offsets:
        trial = {
            'offset' : offset,
            'position' : np.random.randint(min_pos, max_pos)
        }
        trial_list.append(trial)
        
    trial_data = data.TrialHandler(trial_list, n_reps, method = 'random')       
    


except Exception:
    traceback.print_exc()
    


else:
    try:
        for this_trial in trial_data:
            shape1.pos = shape1.pos + (0, this_trial['position'])
            shape1.draw()
            
            shape2.pos = shape2.pos + (0, this_trial['position'] + this_trial['offset'])
            shape2.draw()
            
            win1.flip()
            win2.flip()
            
            subj_input = event.waitKeys(keyList = key_list)
            if subj_input[0] in key_list[0:3]:
                choice = 'below'
            elif subj_input[0] in key_list[3:6]:
                choice = 'above'
            elif subj_input[0] == 'escape':
                break
            else:
                choice = 'unasigned'
            trial_data.addData('choice', choice)
            
        win1.close()
        win2.close()    
        
        df = trial_data.saveAsWideText(fileName = 'vernier_data',
                              appendFile = False,
                              )
        
    except Exception:
        traceback.print_exc()
        win1.close()
        win2.close()