#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 09:17:39 2020

@author: thomassmart
"""


from psychopy import visual, event

window = visual.Window(size = (400,300))
window.color = (-1,-1,-1)
window.flip()

line1 = visual.ShapeStim(window, units = 'pix', lineColor = (1,0,0))
line2 = visual.ShapeStim(window, units = 'pix', lineColor = (0,1,0))

line1.pos = (0,10)
line2.pos = (0,0)

line1.vertices = ((-100,0), (-5,0))
line2.vertices = ((5,0), (100,0))

line1.draw()
line2.draw()

window.flip()

window.getMovieFrame()
window.saveMovieFrames('demo_graphic.png')

event.waitKeys()

window.close()

