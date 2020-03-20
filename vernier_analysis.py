# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:35:49 2020

@author: Experimenter
"""
import vernier_alignment_functions as funs
#import matplotlib.pyplot as plt
import traceback


try:
    df, file_path = funs.csv_to_dataframe_gui()
    
    df['choice_bin'] = df.apply(lambda row: funs.choice_to_value(row), axis = 1)
    
    
    fit_results = {}
    for orientation in df.orientation.unique():
        fit_results[orientation] = funs.vernier_analysis(
                df.sort_values('offset').loc[df['orientation'] == orientation], 
                plot_title = str(orientation),
                )
    
    funs.tabulate_results(df.orientation.unique(), fit_results)
    
    
#    fig, ax = plt.subplots()
#    df.groupby(['offset']).mean().plot(y = 'choice_bin', marker = 'o', linestyle = '', ax = ax)
#    ax.legend().set_visible(False)
#    
#    popt, copt = funs.vernier_fit(df.offset, df.choice_bin, (10,0), ax)

except Exception:
    traceback.print_exc()