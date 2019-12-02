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
from psychopy import data, event
import traceback
import vernier_alignment_functions as funs


## VARIABLES ##

""" user definer orientation"""

theta, rot_mat = funs.rotation_matrix()


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
# build trial parameter dictionaries for psychopy's 'TrialHandler'
for offset in offsets:
    trial = {
        'offset' : offset,
        'position' : np.random.randint(min_pos, max_pos)
    }
    trial_list.append(trial)
    
trial_data = data.TrialHandler(trial_list, n_reps, method = 'random')   


run_type = 'test'


# try/except to prevent window being presented if there is an error in set-up
try:
    
    if run_type == 'test':
        win, shape1, shape2 = funs.initialise_test(line_width/2, 
                                                   line_vertices/2, 
                                                   line_pos/2)
    else:
        mon1, mon2, win1, win2, shape1, shape2 = funs.initialise_oleds(line_width, 
                                                              line_vertices, 
                                                              line_color, 
                                                              line_pos)

except Exception:
    traceback.print_exc()
    


else:
    try:
        for this_trial in trial_data:
            shape1.pos = shape1.pos + rot_mat.dot(np.array((0, this_trial['position'])))
            shape1.draw()
            
            shape2.pos = shape2.pos + rot_mat.dot(np.array((0, this_trial['position'] + this_trial['offset'])))
            shape2.draw()
            
            if run_type == 'test':
                win.flip()
            else:
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
        if run_type == 'test':
            win.close()
        else:
            win1.close()
            win2.close()    
        
        df = trial_data.saveAsWideText(fileName = 'vernier_data',
                              appendFile = False,
                              )
        
    except Exception:
        traceback.print_exc()
        if run_type == 'test':
            win.close()
        else:
            win1.close()
            win2.close()