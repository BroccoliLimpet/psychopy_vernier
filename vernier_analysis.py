# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:35:49 2020

@author: Experimenter
"""
import vernier_alignment_functions as funs
import matplotlib.pyplot as plt

#file_path = r"C:\Users\Experimenter\Documents\Experiments\TS Python\psychopy_vernier\data\tom, ori = 0, date = 22-01-2020, 15-53-07.tsv"   
#df = funs.csv_to_dataframe_filepath(file_path, sort = 'offset')

try:
    df, file_path = funs.csv_to_dataframe_gui()
    
    df['choice_bin'] = df.apply(lambda row: funs.choice_to_value(row), axis = 1)
    
    fig, ax = plt.subplots()
    df.groupby(['offset']).mean().plot(y = 'choice_bin', marker = 'o', linestyle = '', ax = ax)
    ax.legend().set_visible(False)
    
    popt, copt = funs.vernier_fit(df.offset, df.choice_bin, (10,0), ax)

except:
    pass