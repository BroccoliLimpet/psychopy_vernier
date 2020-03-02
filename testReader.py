# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 13:53:23 2020

@author: Experimenter
"""

import pandas as pd

df = pd.read_csv('tom_ninetyDeg_flatMirror_150119.tsv', sep='\t',header=0)
print (df)