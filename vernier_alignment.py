
# -*- coding: utf-8 -*-
"""
Script to present pairs of lines to a subject that are slightly
displaced from one another.

The user is asked to decided whether a certain line is above or below (or to
the left or right) of the other.

Each line is presented on a different OLED monitor and each monitor is
optically filtered - one appears green, the other red. The user can be asked
to decide if the green line is above the red, for example.

Created on Thu Nov 21 15:13:17 2019

@author: Tom Smart
"""

import traceback, os, pyo, time
import numpy as np
import pandas as pd
from psychopy import event
from datetime import datetime


import vernier_alignment_functions as funs
import trial_class


""" Set this variable to 'test' to run in test mode. The shapes are displayed
on this monitor, rather than the external OLEDs. Set variable to 'trial'
(or anyhting else != 'test') to run in trial mode - images will be displayed on OLEDS """
run_type = 'trial'
if run_type != 'test':
    participant_name = input('Participant name: ')
    trial_date = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    file_name = f"{participant_name} {trial_date}"


""" Shape (line) parameters """
shape_parameters = {}
shape_parameters['line_width'] = 2
shape_parameters['line_length'] = 100
shape_parameters['line_color'] = [1, 1, 1]
shape_parameters['line_displacement'] = 10
shape_parameters['screen_position'] = 100
shape_parameters['background_color'] = [-1, -1, -1]
shape_parameters['correction'] = [7, 7]


""" Trial parameters """ 
trial_parameters = {}
offset_low = -15
offset_high = 15
offset_step_size = 5
trial_parameters['offsets'] = np.arange(offset_low, offset_high + offset_step_size, offset_step_size)
trial_parameters['orientations'] = [0, 90, 180, 270]
trial_parameters['nreps'] = 3 


""" Build trial list class - # uses purpose built 'vernier_trial_list' class"""
trial_list = trial_class.vernier_trial_list(trial_parameters['orientations'],
                                            trial_parameters['offsets'],
                                            trial_parameters['nreps'],
                                            )
trial_list.shuffle_trials() 


""" Initialise sounds """
soundserver = pyo.Server(duplex = 0).boot()
soundserver.start()
tone = pyo.Sine(mul = 0.5, freq = 500)


""" Possible subject keyboard inputs """
key_choices = {
        'vert' : ['num_4', 'num_6', '4', '6', 'left', 'right', 'escape'],
        'horiz' : ['num_2', 'num_8', '2', '8', 'up', 'down', 'escape'],
        }


""" Create a list to store trial data """
trial_data = []


""" Initialise monitors, windows and shapes. A try/except/else structures 
should prevent a window being presented if there is an error in set-up (aiming
to avoid kernel death!) """
try:
    wins, line1, line2, shape_parameters = funs.initialise_shapes(shape_parameters, run_type)

    
except Exception:
    traceback.print_exc()


else:
    
    """ Trial starts here """
    try:
        for trial in trial_list:
            line1, line2 = funs.update_shapes(line1, line2, shape_parameters, trial.orientation, trial.offset , run_type)
            line1.draw()
            line2.draw()
            [win.flip() for win in wins]
            
            if trial.orientation in [0, 180]:
                key_choice = event.waitKeys(keyList = key_choices['horiz'])
            elif trial.orientation in [90, 270]:
                key_choice = event.waitKeys(keyList = key_choices['vert'])                
            tone.out()
            time.sleep(0.2)
            tone.stop()
            
            if key_choice[0] == 'escape':
                break
            else:
                trial_data.append({'orientation' : trial.orientation,
                             'offset' : trial.offset,
                             'key_choice' : key_choice[0]
                             })
    
        """ End trial """
        [win.close() for win in wins]
        soundserver.stop()
        df = pd.DataFrame(trial_data)
        fit_results = {}
        for orientation in trial_parameters['orientations']:
            fit_results[orientation] = funs.vernier_analysis(
                    df.sort_values('offset').loc[df['orientation'] == orientation], 
                    plot_title = str(orientation),
                    )
        table = funs.tabulate_results(trial_parameters['orientations'], fit_results)
        if run_type != 'test':
            df.to_csv(os.path.join(os.getcwd(),'data',file_name), sep = '\t')
    
    except Exception:
        """ Close windows """
        [win.close() for win in wins]
        soundserver.stop()
        traceback.print_exc()
        

