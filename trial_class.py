# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 12:13:41 2020

@author: Experimenter
"""

import collections, random
import numpy as np

vernier_trial = collections.namedtuple('trial', ['orientation','offset'])

class vernier_trial_list:
    
    def __init__(self, orientations = np.array([0,90,180,270]), offsets = np.arange(-10,12,2)):
        self.orientations = orientations
        self.offsets = offsets
        self._trials = [vernier_trial(orientation, offset) 
                        for orientation in self.orientations 
                        for offset in self.offsets]
        
    def __len__(self):
        return len(self._trials)
    
    def __getitem__(self, position):
        return self._trials[position]
    
    def __setitem__(self, position, trial):
        self._trials[position] = trial
        
    def sort_by_offset(self):
        self._trials = sorted(self, key = lambda trial : trial.offset)
        
    def shuffle_trials(self):
        self.sort_by_offset()
        new_list = []
        new_trial_list = []
        self.sort_by_offset()
        for trial in self:
            dups = np.nonzero(new_list == trial.orientation)
            dups = np.concatenate([dups[0], dups[0] + 1])
            non_dups = np.setdiff1d(np.arange(0, len(new_list)+1), dups)
            new_pos = non_dups[random.randint(0, len(non_dups)-1)]
            new_list = np.insert(new_list, new_pos, trial.orientation)
            new_trial_list.insert(new_pos, vernier_trial(trial.orientation, trial.offset))
        self._trials = new_trial_list
        
        
my_trial_list = vernier_trial_list()
my_trial_list.shuffle_trials()