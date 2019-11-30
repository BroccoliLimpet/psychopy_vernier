""" This is a psychopy script that uses vernier alignment to align two displays.

Created by Tom Smart, 25 Nov 2019 """ 


from psychopy import visual, event
import numpy as np

win = visual.Window()

shape = visual.ShapeStim(win,
						units = "pix",
						vertices = ((-100,0),(100,0))
						)
shape.draw()

win.flip()

event.waitKeys()

win.close()