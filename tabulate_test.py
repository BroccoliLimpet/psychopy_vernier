# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 13:45:13 2020

@author: Experimenter
"""

from tabulate import tabulate

lst1 = ['a','b','c']
lst2 = [1,2,3]
lst = []
for i in range(len(lst1)):
    lst.append([lst1[i],lst2[i]])
    
    
print(tabulate(lst))