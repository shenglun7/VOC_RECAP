# This source file contains function that are used to analyze the PMF output

import pandas as pd
import numpy as np
from scipy import stats
import datetime as dt
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def pmf_output_to_df(n, p, loc):
    """
    Find the output files from EPAv5.0 PMF model and generate dataframes of PMF profile and contribution.
    input: n = number of species
           p = number of factors
           loc = location of the output files
    output: profile_conc = df of factor profile in concentration, 
            profile_perc_spec = df of factor profile in precentage of each species, profile_perc_factor = df of factor profile in precentage of each factor, 
            contribution = contribution of every factors to daily observed total concentration
    """

    loc_profile = loc+'_profiles.csv'
    loc_contribution = loc+'_contributions.csv'
    profile_conc = pd.read_csv(loc_profile, sep=',', header=None, skiprows=4, nrows=n)
    profile_perc_spec = pd.read_csv(loc_profile, sep=',', header=None, skiprows=2*4+n, nrows=n)
    profile_perc_factor = pd.read_csv(loc_profile, sep=',', header=None, skiprows=3*4+2*n, nrows=n)
    contribution=pd.read_csv(loc_contribution, skiprows=4, sep=',', header=None)

    # drop 1st line, clean df
    profile_conc=profile_conc.drop(columns=[0])
    profile_perc_spec=profile_perc_spec.drop(columns=[0])
    profile_perc_factor=profile_perc_factor.drop(columns=[0])
    contribution=contribution.drop(columns=[0])
    
    # name columns
    column_name = ['Parameter','Factor 1','Factor 2','Factor 3','Factor 4','Factor 5',
                   'Factor 6','Factor 7','Factor 8','Factor 9','Factor 10', 'Factor 11', 'Factor 12']
    column_name2 = ['Date','Factor 1','Factor 2','Factor 3','Factor 4','Factor 5',
                   'Factor 6','Factor 7','Factor 8','Factor 9','Factor 10', 'Factor 11', 'Factor 12']
    profile_conc.columns = column_name[0:p+1]
    profile_perc_spec.columns = column_name[0:p+1]
    profile_perc_factor.columns = column_name[0:p+1]
    contribution.columns = column_name2[0:p+1] 
    
    # rename species
    profile_conc = profile_conc.replace('Trichlorofluoromethane','CFC-11')
    profile_conc = profile_conc.replace('Dichlorodifluoromethane','CFC-12')
    profile_conc = profile_conc.replace('1_1_2-Trichlorotrifluoroethane','CFC-113')
    profile_conc = profile_conc.replace('1_2-Dichloro-1_1_2_2-tetrafluoroethane','CFC-114')

    profile_perc_spec = profile_perc_spec.replace('Trichlorofluoromethane','CFC-11')
    profile_perc_spec = profile_perc_spec.replace('Dichlorodifluoromethane','CFC-12')
    profile_perc_spec = profile_perc_spec.replace('1_1_2-Trichlorotrifluoroethane','CFC-113')
    profile_perc_spec = profile_perc_spec.replace('1_2-Dichloro-1_1_2_2-tetrafluoroethane','CFC-114')
    
    # clean data format
    contribution=contribution.replace(-999,np.nan)
    contribution['Date']=pd.to_datetime(contribution['Date'], format='%m/%d/%y', exact=False)
    
    return profile_conc, profile_perc_spec, profile_perc_factor, contribution


def plot_pmf_profile(n,p,profile_perc_spec,profile_conc, factor_name):
    """
    Plot PMF-solved profile on precentage and concentration of species using output df
    input: n = number of species 
           p = number of factors
           profile_prec_spec = df of factor profile in precentage of each species
           profile_conc = df of factor profile in concentration
           factor_name = a list of factor name
    output: plot of PMF-solved profile on precentage and concentration of species
    """
    plt.rcParams.update({'font.size': 14})
    index = ['a','b','c','d','e','f','g','h','i','j','k','l']

    fig, ax=plt.subplots(nrows=p, figsize=(15,2*p+1), sharey=True, sharex=True)
    
    j=0
    for i in range(p): 
        ax[i].bar(profile_perc_spec.iloc[:,0], profile_perc_spec.iloc[:,j+1], label='% of species')
        
        plt.xticks(rotation = 90) 
        ax[i].set_yticks(np.arange(0, 100, 20))

        if i==0:
            ax[i].text(0.01, 0.6, '('+index[i]+') '+factor_name[i], horizontalalignment='left', verticalalignment='center', transform=ax[i].transAxes, fontweight='bold')
        else:
            ax[i].text(0.01, 0.85, '('+index[i]+') '+factor_name[i], horizontalalignment='left', verticalalignment='center', transform=ax[i].transAxes, fontweight='bold')

        # second y axis for concentration
        ax1=ax[i].twinx()
        ax1.scatter(profile_conc.iloc[:,0], profile_conc.iloc[:,j+1], color='red',label='Concentration')
        if i == 0:
            ax1.legend(loc='upper right')
        j=j+1
    
    ax[0].legend(loc='upper left') 
    fig.text(0.09, 0.5, '% of species', va='center', rotation='vertical')
    fig.text(0.93, 0.5, 'Concentration (ppbv)', va='center', rotation='vertical')
    #plt.tight_layout()

    plt.show()
    return fig


def plot_factor_time_series(n,p,contribution, factor_name):
    """
    Plot time series of PMF-solved factor in normalized contribution
    input: n = number of species
           p = number of factors
           contribution = contribution of every factors to daily observed total concentration
           factor_name = a list of factor name
    output: plot of contribution time series
    """
    
    import matplotlib.dates as mdates
    plt.rcParams.update({'font.size': 14})
    index = ['a','b','c','d','e','f','g','h','i','j','k','l']

    fig, ax=plt.subplots(nrows=p, figsize=(13,2*p-1), sharex=True)

    j=0
    for i in range(p):
        ax[i].plot(contribution['Date'], contribution.iloc[:,j+1])
        ax[i].scatter(contribution['Date'], contribution.iloc[:,j+1],s=20)
        #ax[i].set_title(factor_name[i], fontweight='bold')
        j=j+1
    
    # Highlight weekends based on the x-axis units
        xmin, xmax = ax[i].get_xlim()
        days = np.arange(np.floor(xmin), np.ceil(xmax)+2)
        weekends = [(dt.weekday()>=5) for dt in mdates.num2date(days)]
        ax[i].fill_between(days, *ax[i].get_ylim(), where=weekends, facecolor='red', alpha=.1, label='Weekend')
        ax[i].set_xlim(xmin, xmax) # set limits back to default values    
    
    # add factor name
        ax[i].text(0.01, 0.85, '('+index[i]+') '+factor_name[i], 
                   horizontalalignment='left', verticalalignment='center', 
                   transform=ax[i].transAxes, fontweight='bold')

    ax[0].legend()    
    #fig.text(0.02, 0.5, 'Normalized contribution', va='center', rotation='vertical')
    plt.xlabel('Date')
    
    plt.tight_layout()
    plt.show()
    return fig


def reorder_factor(df, new_order):
    """
    Re-order the factor on columns in df based on the name of factors 
    Input: p = number of factors 
           df = data frame needs reorder
           new_order = a list of new ordered column
    Output: a reordered df
    """

    # get number of factor
    p = df.shape[1]-1
    
    # get old order
    cols = df.columns.tolist()
    
    # re-order by new-order
    cols[1:p+1] = new_order
    df = df[cols]

    return df


def plot_CPF(new_order, contribution, figname):
    """
    function to calculate cpf for each factor and plo  t as windrose
    Input: new_order = reordered factor
           contribution = df from treat_PMF_output()
           figname = specific file name for windrose
    Output: windrose
    """

    # merge contribution with wind profile
    contribution_wind=contribution.merge(df_wind_filter[['Date','drct', 'sped']], on='Date', how='left')

    # bin contribution by wind direction
    contribution_wind.loc[contribution_wind['drct'].notnull(),'bin']=\
        pd.cut(contribution_wind.loc[contribution_wind['drct'].notnull(),'drct'], np.arange(0,360,30))

    df = contribution_wind

    # count total events in every factor in every binned wind direction
    df_CPF = df.groupby('bin').count().reset_index()
    df_CPF_count_total = df_CPF.drop(columns={'Date','drct','sped'})

    # count events in upper 25% for every factor in every binned wind direction
    df_CPF_count_upper = df_CPF.drop(columns={'Date','drct','sped'})
    for col in df.columns:
        if 'Factor' in col:
            for bin_val in df['bin'].unique():
                threshold = df.loc[:, col].quantile(0.75)
                count_upper = df[(df['bin']==bin_val)&(df[col]>threshold)].shape[0]
                df_CPF_count_upper.loc[df_CPF_count_upper['bin']==bin_val, col] = count_upper  
            
    # calculate mean of bin for windrose plotting
    df_CPF_count_upper['bin_mean']=df_CPF_count_upper.bin.apply(lambda x: x.mid)
    df_CPF_count_total['bin_mean']=df_CPF_count_total.bin.apply(lambda x: x.mid)
    
    # screen out wind direction with total days < 3
    df_CPF_count_total = df_CPF_count_total.replace(1,np.nan)
    df_CPF_count_total = df_CPF_count_total.replace(2,np.nan)
    
    
    # calculate CPF for each factor
    df_ratio = df_CPF_count_upper.filter(like='Factor', axis=1).\
                   divide(df_CPF_count_total.filter(like='Factor', axis=1))
    df_ratio['bin_mean'] = df_CPF_count_upper['bin_mean']
    
    # plot CPF 
    import plotly.express as px
    for i in new_order:  
        fig = px.bar_polar(df_ratio, r=i,
                           theta='bin_mean',
                           width=400, height=400)
        fig.update_layout(margin=dict(l=50, r=50, t=50, b=50),
                          title={'text': i})
        fig.show()
        
