# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 14:30:44 2020

@author: Experimenter
"""

import vernier_alignment_functions as funs
#import trial_class
import numpy as np
import traceback
from psychopy import event


""" Shape (line) parameters """
shape_parameters = {}
shape_parameters['line_width'] = 2
shape_parameters['line_length'] = 100
shape_parameters['line_color'] = [1, 1, 1]
shape_parameters['line_displacement'] = 10
shape_parameters['screen_position'] = 100
shape_parameters['background_color'] = 0.8 * np.array([-1, -1, -1])
shape_parameters['correction'] = [4, 0]

orientation = 270


try:
    wins, line1, line2, shape_parameters = funs.initialise_shapes(shape_parameters)

    
except Exception:
    traceback.print_exc()
    
else:
    
    try:
        line1, line2 = funs.update_shapes(line1, line2, shape_parameters, orientation = orientation)
        line1.draw()
        line2.draw()
        [win.flip() for win in wins]
        event.waitKeys()
        [win.close() for win in wins]
    
    except Exception:
        [win.close() for win in wins]
        traceback.print_exc()
        