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


def integer_input(message = "Please enter an integer", integer_range = None):
    """
    Take an input from user and check that it is an integer.
    
    Keyword arguments:
    message -- asks user for input
    integer_range -- optional integer range
    
    Returns:
    integer from user
    
    """
    
#    integer = []
#    while not (integer > integer_range[0] and integer < integer_range[1]):
    
    try:
        integer = int(input(message))
    except Exception:
        print("Please enter an integer\n")
    else:
        return integer
            



# constants
ORIENTATION = integer_input("Please enter the required orientation: ", [0, 360])
THETA = np.radians(ORIENTATION)
R = np.array([[np.cos(THETA), -np.sin(THETA)],[np.sin(THETA), np.cos(THETA)]])

MIN_POS = -20   # minimum central position of line pair
MAX_POS = 20    # maximum central position of line pair

OFFSET_LOW = -10   # largest negative offset (i.e. green below red)
OFFSET_HIGH = 10   # largest positive offset
OFFSET_STEP_SIZE = 2  # offset increment
OFFSETS = np.arange(OFFSET_LOW, OFFSET_HIGH + OFFSET_STEP_SIZE, OFFSET_STEP_SIZE)   # generate array of possible offset values

N_REPS = 1  # trial repeats
KEY_LIST = ['num_1', 'num_2', 'num_3', 'num_7', 'num_8', 'num_9', 'escape']    # possible keyboard entries

LINE_WIDTH = 5 # width of line
LINE_LENGTH = 300   # length of line
LINE_VERTICES_RAW = np.array(((-LINE_LENGTH/2, 0), (LINE_LENGTH/2, 0)))   # line coordinates
LINE_VERTICES = R.dot(LINE_VERTICES_RAW)
LINE_DISPLACEMENT = 25  # separation of line ends

LINE_COLOR = [-1, -1, -1]
LINE_POS_RAW = (LINE_LENGTH/2 + LINE_DISPLACEMENT, 0)
LINE_POS = R.dot(LINE_POS_RAW)
# variables

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
                             lineWidth = LINE_WIDTH,
                             vertices = LINE_VERTICES,
                             lineColor = LINE_COLOR,   # adust brightness (correct terminology? probs not)
                             pos = LINE_POS, # one of the screens is viewed backwards...88
                             )
                             
    shape2 = visual.ShapeStim(win2,
                             units = "pix",
                             lineWidth = LINE_WIDTH,
                             vertices = LINE_VERTICES,
                             lineColor = LINE_COLOR,
                             pos = LINE_POS,
                             )
    
 
    
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
    try:
        for this_trial in trial_data:
            shape1.pos = shape1.pos + (0, this_trial['position'])
            shape1.draw()
            
            shape2.pos = shape2.pos + (0, this_trial['position'] + this_trial['offset'])
            shape2.draw()
            
            win1.flip()
            win2.flip()
            
            SUBJ_INPUT = event.waitKeys(keyList = KEY_LIST)
            if SUBJ_INPUT[0] in KEY_LIST[0:3]:
                choice = 'below'
            elif SUBJ_INPUT[0] in KEY_LIST[3:6]:
                choice = 'above'
            elif SUBJ_INPUT[0] == 'escape':
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