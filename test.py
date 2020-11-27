#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import vernier_alignment_functions as funs

trial_list = funs.vernier_trial_list()


class test_trialList(unittest.TestCase):
    
    trial_list = funs.vernier_trial_list()
    
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
        



if __name__ == '__main__':
    unittest.main()