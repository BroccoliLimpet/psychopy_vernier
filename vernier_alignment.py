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
import trial_class


""" Set this variable to 'test' to run in test mode. The shapes are displayed
on this monitor, rather than the external OLEDs. """

run_type = 'trial'

""" Shape (line) parameters """
shape_parameters = {}
shape_parameters['line_width'] = 2
shape_parameters['line_length'] = 100
shape_parameters['line_color'] = [1, 1, 1]
shape_parameters['line_displacement'] = 10
shape_parameters['screen_position'] = 100
shape_parameters['background_color'] = 0.8 * np.array([-1, -1, -1])



""" Trial parameters """ 
trial_parameters = {}
trial_parameters['n_reps'] = 5 
 

""" The offset between the two lines (that is, the amount by which the two 
lines do not line up) change between each trial. Parameters set here. """
# largest negative offset (i.e. green below red)
offset_low = -10
# largest positive offset
offset_high = 10   
# offset increment
offset_step_size = 20
# generate array of possible offset values
trial_parameters['offsets'] = np.arange(offset_low, offset_high + offset_step_size, offset_step_size)
trial_parameters['orientations'] = [0, 90, 180, 270]


""" Build trial list class """
trial_list = trial_class.vernier_trial_list(trial_parameters['orientations'], trial_parameters['offsets'])
trial_list.shuffle_trials()


""" Initialise sounds """
soundserver = pyo.Server(duplex = 0).boot()
soundserver.start()
tone = pyo.Sine(mul = 0.5, freq = 500)


""" Possible subject keyboard inputs """
key_list = ['num_1', 'num_2', 'num_3', \
            'num_4', 'num_5', 'num_6', \
            'num_7', 'num_8', 'num_9', \
            'escape']


""" Initialise monitors, windows and shapes. A try/except/else structures 
should prevent a window being presented if there is an error in set-up (aiming
to avoid kernel death!) """

try:
    wins, line1, line2, shape_parameters = funs.initialise_shapes(shape_parameters, run_type)

    
except Exception:
    traceback.print_exc()
    
else:
    try:
        for trial in trial_list:
            line1, line2 = funs.update_shapes(line1, line2, shape_parameters, trial, run_type)
            line1.draw()
            line2.draw()
            [win.flip() for win in wins]
            event.waitKeys()
        [win.close() for win in wins]
        soundserver.stop()
    
    except Exception:
        """ Close windows """
        [win.close() for win in wins]
        soundserver.stop()
        traceback.print_exc()
        
    
    
    # """ Trial starts here. """

    # try:
    #     line1_init = line1.pos
    #     line2_init = line2.pos
    #     for this_trial in trial_list:
            
            
    #         line1_shift = np.array([[0], [this_trial['position']]])
    #         line2_shift = np.array([[0], [this_trial['position'] + this_trial['offset']]])

    #         if run_type == 'test':
    #             line1.pos = line1.pos + rotate_mat.dot(line1_shift).transpose()
    #             line1.draw()
                
    #             line2.pos = line2.pos + rotate_mat.dot(line2_shift).transpose()
    #             line2.draw()                
                
    #         else:
    #             line1.pos = line1_init + rotate_mat.dot(line1_shift).transpose()
    #             line1.draw()
                
    #             line2.pos = line2_init + reflect_mat.dot(rotate_mat.dot(reflect_mat.dot(line2_shift))).transpose()
    #             line2.draw()
            
    #         if run_type == 'test':
    #             win.flip()
            
    #         else:
    #             win1.flip()
    #             win2.flip()
            
    #         choice = event.waitKeys(keyList = key_list)
    #         tone.out()
    #         time.sleep(0.2)
    #         tone.stop()
            
    #         if choice[0] == 'escape':
    #             break
    #         else:
    #             trial_data.addData('choice', choice[0])
                
            
            
            
    #     if run_type == 'test':
    #         win.close()
    #     else:
    #         win1.close()
    #         win2.close()    
        
    #     if run_type != 'test':
    #         """ Save output as a text doc and create a panda dataframe"""
    #         df = trial_data.saveAsWideText(fileName = file_name,
    #                               appendFile = False,
    #                               )
    #         fig, ax = funs.vernier_plot(df, ticks = offsets)
    #         popt, copt = funs.vernier_fit(list(df.offset), list(df.choice_bin), ax)

                              
    # except Exception:
    #     """ Close windows """
    #     traceback.print_exc()
    #     if run_type == 'test':            win.close()
    #     else:
    #         win1.close()
    #         win2.close()
    #         soundserver.stop()            