#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest, json, psychopy

import numpy as np

import vernier_alignment_functions as funs

run_type = 'test'
trial_list = funs.vernier_trial_list()


with open('default_shape_parameters.json') as f:
    shape_parameters = json.load(f)

wins, line1, line2, shape_parameters = funs.initialise_shapes(shape_parameters, run_type)


class test_trialList(unittest.TestCase):
    
    def test_length(self):
        self.assertTrue(hasattr(trial_list, "__len__"))
        
    def test_getItem(self):
        self.assertTrue(hasattr(trial_list, "__getitem__"))
        
    def test_sortByOffset(self):
        trial_list.sort_by_offset()
        self.assertEqual(trial_list._trials[0].offset, trial_list._trials[1].offset)
        
    def test_shuffleTrials(self):
        trial_list.shuffle_trials()
        self.assertTrue(trial_list._trials[0].orientation != trial_list._trials[1].orientation)
        

class test_initShapes(unittest.TestCase):
    
    def test_winType(self, window = wins[0]):
        self.assertTrue(type(window) == psychopy.visual.window.Window)
        
    def test_shape1Type(self):
        self.assertTrue(type(line1 == psychopy.visual.shape.ShapeStim))
    
    def test_shape2Type(self):
        self.assertTrue(type(line2 == psychopy.visual.shape.ShapeStim))
        
    def test_line1Length(self):
        self.assertTrue(np.diff((line1.vertices[0][1], line1.vertices[1][1]))[0] == shape_parameters['line_length'])
        
    # def test_line1Pos(self):
    #     self.assertTrue(line1.pos[0] == 60)
        
    # def test_line2Pos(self):
    #     self.assertTrue(line2.pos[0] == 60)
        
        
class test_updateShapes(unittest.TestCase):
    
    offset = 10 
    
    funs.update_shapes(line1, line2, shape_parameters, orientation = 90, offset = offset, run_type = 'test')

        
    def test_line1Pos(self):
        self.assertTrue(line1.pos[0] == -100)
        
    def test_line2Pos(self):
        self.assertTrue(line2.pos[0] == -110)
        
    def test_Offset(self, offset = offset):
        self.assertEqual(abs(line2.pos[0] - line1.pos[0]), offset)


[win.close() for win in wins]
    



if __name__ == '__main__':
    unittest.main()