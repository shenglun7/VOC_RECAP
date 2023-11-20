# This source code contains function treat the measured VOC concentration data in Redlands
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_time_series(df_voc, voc_list):
    """
    This function generate the time series plot (scatter + line) for a list of VOCs in same x and y axis with different color.
    Input: df_voc: the dataframe contains the VOC concentration data, with columns: 'Sample date'(in dt format), 'Parameter', 'Value'
           voc_list: the list of VOCs to be plotted
    Output: fig, time series plot
    """

    df_plot = df_voc[df_voc['Parameter'].isin(voc_list)].reset_index(drop=True)

    fig, ax=plt.subplots(figsize=(6,3))
    for i in voc_list:
        ax.scatter(df_plot.loc[df_plot['Parameter']==i,'Sample date'], 
                   df_plot.loc[df_plot['Parameter']==i,'Value'], 
                   label=i, s=10)
        ax.plot(df_plot.loc[df_plot['Parameter']==i,'Sample date'], 
                df_plot.loc[df_plot['Parameter']==i,'Value'])

    # shaded weekends area
    date_list = pd.date_range(start='2021-07-10', end='2021-10-31', freq='D')
    for i in range(len(date_list)):
        if date_list[i].weekday()==6:
            ax.axvspan(date_list[i]-pd.Timedelta(days=0),
                       date_list[i]+pd.Timedelta(days=1.2),
                       facecolor='grey', alpha=0.3)
            
    ax.set_xlabel('Date')
    ax.set_ylabel('Concentration (ppbv)')
    plt.xticks(rotation=25) 
    plt.legend()

    fig.show()
    return fig
