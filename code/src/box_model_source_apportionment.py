# This source file contains function that are used to analyze the box model data (input & output)

import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt
import os
import matplotlib.pyplot as plt


def treat_box_model_output(filepath):
    """
    transfer box model output results to df
    input: filepath = location of the output file
    output: df = df of box model output ['Date','Time','O3','O3_X1','O3_X2','O3_X3','O3_X4', ...], where Time = time in UV reaction, O3 = vanilla O3, O3_X1 = O3 from X1, etc.
    """
    
    # df to store O3 source concentration
    df = pd.DataFrame(columns=['Date','Time','O3','O3_X1','O3_X2','O3_X3','O3_X4',
                               'O3_X5','O3_X6','O3_X7','O3_X8','O3_X9'])
    
    # get O3 source concentration in date and time
    O3_source_name = ['O3','O3_X1','O3_X2','O3_X3','O3_X4',
                      'O3_X5','O3_X6','O3_X7','O3_X8','O3_X9']

    with open(filepath) as f:
        contents = f.readlines()

    list_time = [s for s in contents if 'Results at time' in s]
    df.loc[0,'Time'] = 0.0
    for i in range(len(list_time)):
        df.loc[i+1,'Time'] = float(list_time[i].split(' ')[-1])

    for i in O3_source_name:
        name_in_str = ' '+i+' '
        list_O3 = [s for s in contents if name_in_str in s]
        for j in range(len(list_O3)):
            df.loc[j,i] = list_O3[j][33:33+13]
    
    # get date
    date = filepath.split('/')[-1][8:18]
    df['Date'] = pd.to_datetime(date)
    for i in df.columns[2:]:
        df[i] = df[i].astype(float)
    df['Time'] = df['Time'].astype(int)
    
    return df


