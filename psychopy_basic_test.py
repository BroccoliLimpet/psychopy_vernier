# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:12:19 2020

@author: Experimenter
"""

from psychopy import visual, event

win = visual.Window()

win.flip()

event.waitKeys()

win.close()