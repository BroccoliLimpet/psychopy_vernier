# -*- coding: utf-8 -*-
"""
Script to present horizontal (or vertical) lines to a subject that are slightly
displaced from one another.

The user is asked to decided whether a certain line is above or below (or to
the left or right) of the other.

Each line is presented on a different OLED monitor and each monitor is
optically filtered - one appears green, the other red. The user can be asked
to decide if the green line is above the red, for example.

Created on Thu Nov 21 15:13:17 2019

@author: Tom Smart
"""

import numpy as np
from psychopy import data, event
import traceback
import vernier_alignment_functions as funs
from datetime import datetime
import pyo
import time


""" This variable can be used to enter the trial mode which displays lines on this
monitor, rather than the OLEDS. The size and displacements of the lines are
scaled down by a factor of two in the test mode. """

run_type = 'test'

shape_parameters = {}

""" user defines orientation - this determines the orientation of the two 
lines"""
shape_parameters['theta'] = np.radians(int(input("Enter orientation in degrees: ")))


""" Establish constants """
pix2deg = 0.0021
pix2arcmin = pix2deg / 60 
rotate_mat = funs.rotation_matrix(shape_parameters['theta'])
reflect_mat = funs.reflection_matrix()


""" The position of the two lines change randomly between each trial. 
Parameters are set here."""
# minimum central position of line pair
min_pos = -20
# maximum central position of line pair  
max_pos = 20    


""" Line appearence parameters """
shape_parameters['line_width'] = 2
shape_parameters['line_length'] = 100
   
""" separation of line ends """
shape_parameters['line_displacement'] = 12  

""" colors """
shape_parameters['line_color'] = [1, 1, 1]
shape_parameters['background_color'] = 0.8 * np.array([-1, -1, -1])

""" position lines on one side of screen """
screen_position_offset = -200
shape_parameters['screen_position'] = np.array([[0], [screen_position_offset]])


""" Line vertices aranged here as [[x1, x2, ..., xn], [y1, y2, y3, ..., yn]] 
to allow multiplication by rotation matrix. For Psychopy, this needs to be 
transposed to become [[x1, y1], [x2,y2], ..., [xn, yn]]. """

# line_vertices = np.array([[-line_length/2, line_length/2], [0, 0]])
# line_pos = np.array([[line_length/2 + line_displacement], [0]])


""" The number of trials and possible subject keyboard inputs"""
# trial repeats
n_reps = 5
key_list = ['num_1', 'num_2', 'num_3', \
            'num_4', 'num_5', 'num_6', \
            'num_7', 'num_8', 'num_9', \
            'escape']  

""" The offset between the two lines (that is, the amount by which the two 
lines do not line up) change between each trial. Parameters set here. """

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

""" Add additional trial information """
if run_type == 'trial':
    participant_name = input('Participant name: ')
    trial_date = datetime.now().strftime("%d-%m-%Y, %H-%M-%S")
    trial_data.extraInfo = {
            'participant' : participant_name,
            'date' : trial_date,
            'orientation' : shape_parameters['theta'],
            'screen_position' : shape_parameters['screen_position'],
            }
    
    file_name = f"data\{participant_name}, ori = {int(np.rad2deg(shape_parameters['theta']))}, date = {trial_date}"




"""
Iitialise sounds
"""
soundserver = pyo.Server(duplex = 0).boot()
soundserver.start()
tone = pyo.Sine(mul = 0.5, freq = 500)


""" Initialies monitors, windows and shapes. A try/except/else structures 
should prevent a window being presented if there is an error in set-up (aiming
to avoid kernel death """

try:
#    pass
    if run_type == 'test':
        win, line1, line2, shape_parameters['shape_vertices'], shape_parameters['shape_position']= funs.initialise_test(shape_parameters, rotate_mat, reflect_mat)
        
    else:
        mon1, mon2, win1, win2, line1, line2 = funs.initialise_oleds(line_width, 
                                                              line_vertices, 
                                                              line_color, 
                                                              line_pos,
                                                              rotate_mat,
                                                              background_color,
                                                              )

    
except Exception:
    traceback.print_exc()


    
else:
    """ Trial starts here. """

    try:
        line1_init = line1.pos
        line2_init = line2.pos
        for this_trial in trial_data:
            
#            print("line1 = " + str(line1.pos) + "\nline2 = " + str(line2.pos) + "\n")
#            print("position = " + str(this_trial['position']) + ", offset = " + str(this_trial['offset']))
            
            line1_shift = np.array([[0], [this_trial['position']]])
            line2_shift = np.array([[0], [this_trial['position'] + this_trial['offset']]])

            if run_type == 'test':
                line1.pos = line1.pos + rotate_mat.dot(line1_shift).transpose()
                line1.draw()
                
                line2.pos = line2.pos + rotate_mat.dot(line2_shift).transpose()
                line2.draw()                
                
            else:
                line1.pos = line1_init + rotate_mat.dot(line1_shift).transpose()
                line1.draw()
                
                line2.pos = line2_init + reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(line2_shift))).transpose()
                line2.draw()
            
            if run_type == 'test':
                win.flip()
            else:
                win1.flip()
                win2.flip()
            
            choice = event.waitKeys(keyList = key_list)
            tone.out()
            time.sleep(0.2)
            tone.stop()
            
            if choice[0] == 'escape':
                break
            else:
                trial_data.addData('choice', choice[0])
                
            
            
            
        if run_type == 'test':
            win.close()
        else:
            win1.close()
            win2.close()    
        
        if run_type != 'test':
            """ Save output as a text doc and create a panda dataframe"""
            df = trial_data.saveAsWideText(fileName = file_name,
                                  appendFile = False,
                                  )
            fig, ax = funs.vernier_plot(df, ticks = offsets)
            popt, copt = funs.vernier_fit(list(df.offset), list(df.choice_bin), ax)

                              
    except Exception:
        """ Close windows """
        traceback.print_exc()
        if run_type == 'test':            win.close()
        else:
            win1.close()
            win2.close()
            soundserver.stop()
            