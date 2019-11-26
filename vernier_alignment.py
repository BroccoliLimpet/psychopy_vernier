# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:13:17 2019

@author: Tom Smart
"""

import numpy as np
from psychopy import data, visual, event

try:
    win = visual.Window(color = [0, 0, 0])
    
    shape = visual.ShapeStim(win,
                             vertices = ((-100, 0), (100, 0)),
                             lineColor = [-1, -1, -1],
                             )
    
    
    
    OFFSETS = np.arange(-10,12,2)
    trial = {}
    trial_list = []
    N_REPS = 1
    
    for value in OFFSETS:
        trial = {
            'offset' : value,
            'position' : np.random.randint(-20, 20)
        }
        trial_list.append(trial)
        
    trial_data = data.TrialHandler(trial_list,
                                            N_REPS,
                                            method = 'random',
                                            )
except:
    print("Error in set-up")
    
else:
    shape.draw()
    win.flip()
                                         
    for this_trial in trial_data:
    #    print(this_trial['offset'])
    #    trial_data.addData('position', np.random.randint(0,9))
        shape.pos = (0, np.random.randint(-20,20))
        shape.draw()
        win.flip()
        choice = event.waitKeys()
        trial_data.addData('choice', choice)
        
    win.close()    
    
    trial_data.saveAsText(fileName = 'testData',
                          dataOut = 'n')
    
#    trial_data.saveAsExcel(fileName = 'testData')