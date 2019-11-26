# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:13:17 2019

@author: Tom Smart
"""

import numpy as np
from psychopy import data, visual, event

try:
    win = visual.Window(color = [0, 0, 0])
    
    shape1 = visual.ShapeStim(win,
                             units = "pix",
                             vertices = ((-100, 0), (100, 0)),
                             lineColor = [1, -1, -1],
                             )
                             
    shape2 = visual.ShapeStim(win,
                             units = "pix",
                             vertices = ((-100, 0), (100, 0)),
                             lineColor = [-1, 1, -1],
                             )
    
    
    MIN_POS = -20
    MAX_POS = 20
    OFFSETS = np.arange(-10,12,2)
    trial = {}
    trial_list = []
    N_REPS = 3
    
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
except:
    print("Error in set-up")
    
else:
    shape1.draw()
    win.flip()
                                         
    for this_trial in trial_data:
    #    print(this_trial['offset'])
    #    trial_data.addData('position', np.random.randint(0,9))
        shape1.pos = (0, this_trial['position'])
        shape1.draw()
        shape2.pos = (0, this_trial['position'] + this_trial['offset'])
        shape2.draw()
        win.flip()
        if event.waitKeys(keyList = ['up','down'])[0] == 'up':
            choice = 'above'
        else:
            choice = 'below'
        trial_data.addData('choice', choice)
        
    win.close()    
    
    trial_data.saveAsText(fileName = 'vernier_data',
                          stimOut = ['offset', 'position'],
                          dataOut = ['choice_raw'])
    
#    trial_data.saveAsExcel(fileName = 'testData')