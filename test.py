#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import vernier_alignment_functions as funs

trial_list = funs.vernier_trial_list()

class test_trialList(unittest.TestCase):
    
    trial_list = funs.vernier_trial_list()
    
    def test_length(self):
        self.assertEqual(len(trial_list), len(trial_list.offsets) * len(trial_list.orientations), "equal")
        
    def test_getItem(self):
        self.assertTrue(trial_list[0].orientation == 0)
        
    def test_sortByOffset(self):
        trial_list.sort_by_offset()
        self.assertEqual(trial_list._trials[0].offset, trial_list._trials[1].offset)



if __name__ == '__main__':
    unittest.main()