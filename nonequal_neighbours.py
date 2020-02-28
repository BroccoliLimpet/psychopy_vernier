# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:57:17 2020

@author: Experimenter
"""

import numpy as np
import random, pdb

pos = np.arange(1,5)
reps = 11
lst = np.tile(pos,reps)
new_lst = np.array([])


for j in range(len(lst)):
    pdb.set_trace()
    dups = np.nonzero(new_lst == lst[j])
    dups = np.concatenate([dups[0], dups[0] + 1])
    non_dups = np.setdiff1d(np.arange(0, len(new_lst)+1), dups)
    new_pos = non_dups[random.randint(0, len(non_dups)-1)]
    new_lst = np.insert(new_lst, new_pos, lst[j])

# new_lst = np.zeros(lst.shape)
# for item in lst:
#     dups = np.nonzero(new_lst == item)
#     dups = np.concatenate([dups[0], dups[0] + 1])
#     non_dups = np.setdiff1d(np.arange(0, len(new_lst)-1), dups)
#     new_pos = non_dups[random.randint(0, len(non_dups)-1)]    
#     np.put(new_lst, new_pos, item)shu