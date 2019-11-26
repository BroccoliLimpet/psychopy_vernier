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

# try/except to prevent window being presented if there is an error in 
try:
    # Gain access to calibration/screen information
    mon1 = monitors.Monitor('whiteOLED_1_SADK_luma1200')  
    mon2 = monitors.Monitor('whiteOLED_2_SADK_luma1200')  
    
    # Initialise windows  
    win1 = visual.Window(size = mon1.getSizePix(),
                        monitor = mon1,
                        winType = "pyglet",
                        screen = 2)
                     
    win2 = visual.Window(size = mon2.getSizePix(),
                        monitor = mon2,
                        winType = "pyglet",
                        screen = 1)
    
    # Create lines to be presented on screens
    
    LINE_WIDTH = 10
    shape1 = visual.ShapeStim(win1,
                             units = "pix",
                             lineWidth = LINE_WIDTH,
                             vertices = ((-100, 0), (100, 0)),
                             lineColor = [1, -1, -1],
                             )
                             
    shape2 = visual.ShapeStim(win2,
                             units = "pix",
                             lineWidth = LINE_WIDTH,
                             vertices = ((-100, 0), (100, 0)),
                             lineColor = [-1, 1, -1],
                             )
    
    # constants
    MIN_POS = -20
    MAX_POS = 20
    OFFSETS = np.arange(-10,12,2)
    trial = {}
    trial_list = []
    N_REPS = 1
    KEY_LIST = ['num_1','num_2','num_3','num_7','num_8','num_9']
    
    # build trial parameter dictionaries for psychopy's 'TrialHandler'
    for offset in OFFSETS:
        trial = {
            'offset' : offset,
            'position' : np.random.randint(MIN_POS, MAX_POS)
        }
        trial_list.append(trial)
        
    trial_data = data.TrialHandler(trial_list,
                                    N_REPS,
                                    method = 'random',
                                    )
except Exception:
    traceback.print_exc()
    
    
else:
    for this_trial in trial_data:
        shape1.pos = (0, this_trial['position'])
        shape1.draw()
        
        shape2.pos = (0, this_trial['position'] + this_trial['offset'])
        shape2.draw()
        
        win1.flip()
        win2.flip()
        
        SUBJ_INPUT = event.waitKeys(keyList = KEY_LIST)
        if SUBJ_INPUT in KEY_LIST[0:3]:
            choice = 'above'
        elif SUBJ_INPUT in KEY_LIST[3:6]:
            choice = 'below'
        trial_data.addData('choice', choice)
        
    win1.close()
    win2.close()    
    
    trial_data.saveAsText(fileName = 'vernier_data',
                          stimOut = ['offset', 'position'],
                          dataOut = ['choice_raw'])
    
#    trial_data.saveAsExcel(fileName = 'testData')
# NEW BRANCH