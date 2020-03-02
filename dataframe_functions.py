# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:50:22 2020

@author: Experimenter
"""

import tkinter as tk
from tkinter import filedialog
import pandas as pd

def csv_to_dataframe_filepath(file_path, **kwargs):
    # read file in as data frame
    df = pd.read_csv(file_path, sep = "\t")
    
    # if sort argument passed in, sort dataframe on the value given
    if kwargs:
        df = df.sort_values(kwargs["sort"])
    
    # return the dataframe
    return df


def csv_to_dataframe_gui(**kwargs):
    # user finds file through GUI
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfile()
    
    # read file in as data frame
    df = pd.read_csv(file_path, sep = "\t")
    
    # if sort argument passed in, sort dataframe on the value given
    if kwargs:
        df = df.sort_values(kwargs["sort"])
    
    # return the dataframe
    return df

#def csv_to_dataframe(options):
#    file_path = options["file_path"]
#    sort_on = options["sort_on"]
    
    


def choice_to_value(row):
    if row['choice'] in (['num_1', 'num_4', 'num_7'] or ['num_7', 'num_8', 'num_9']):
        return 1
    elif row['choice'] in (['num1', 'num_2', 'num_3'] or ['num_3', 'num_6', 'num_9']):
        return -1
    



#options = {"sort_on" : "offset", 
#           "file_path" : r"C:\Users\Experimenter\Documents\Experiments\TS Python\psychopy_vernier\tom_ninetyDeg_flatMirror_150119.tsv"}
#csv_to_dataframe(options)