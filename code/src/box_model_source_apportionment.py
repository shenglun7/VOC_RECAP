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


def get_initial_conc(filepath):
    """
    get initial concentration of VOCs
    input: filepath = location of the output file
    output: df = df of initial concentration ['Date','Time','O3','VOCs'], where Time = time in UV reaction, O3 = vanilla O3, VOCs = vanilla VOCs
    """

    para_number = 1147  # number of parameters in the box model
    df = pd.read_csv(filepath, skiprows=1, nrows=para_number, 
                     header=None,delim_whitespace=True)
    df.columns = ['Number','Parameter','Value']

    return df


def get_daily_source_conc(date, df, list_saprc):
    """
    get daily concentration of every source of VOCs from a df of box model output
    input: date = date of the box model output
           df = df of box model output: ['Number','Parameter','Value']
           list_saprc = list of SAPRC parameters name accounted for calculation
    output: df_out = df:['Date','Factor','Conc']
    """

    df_source_conc = pd.DataFrame(columns=['Date','Factor','Conc'])
    nspecies = 9
    for i in range(nspecies):
        list_saprc_X = [list_saprc + '_X' + str(i+1) for list_saprc in list_saprc]
        sum_conc = df.loc[df['Parameter'].isin(list_saprc_X), 'Value'].sum()
        df_source_conc = \
            df_source_conc.append({'Date':date, 'Factor': 'X'+str(i+1), 'Conc': sum_conc},
                                  ignore_index=True)
        
    return df_source_conc