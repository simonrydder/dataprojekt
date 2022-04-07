"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Main.py

Discribtion:    
"""

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Import other files
from Metrics2 import Metrics_Info


# Functions
def myFig(data, title = ''):
    
    fig = plt.figure(constrained_layout = True)
    fig.suptitle(title)

    rowNames = list(data.Comparison.unique())
    colNames = list(data.Metric.unique())
    rows = len(rowNames)
    cols = len(colNames)
    
    grp = data.groupby(by = ['Comparison', 'Metric'])
    mean = grp.mean()
    std = grp.std()
    
    subfigs = fig.subfigures(nrows = rows, ncols = 1)
    for row, subfig in enumerate(subfigs):
        Comp = rowNames[row]
        subfig.suptitle(' vs '.join(Comp.split('vs')))

        axs = subfig.subplots(nrows = 1, ncols = cols)
        for col, ax in enumerate(axs):
            Metric = colNames[col]
            ax.set_title(f'{Metric}')

            temp = data[data.Comparison == Comp]
            temp = temp[temp.Metric == Metric]
            boxdata = temp.iloc[:, 2:]

            rowMean = mean.loc[(Comp, Metric), :]
            rowStd = std.loc[(Comp, Metric), :]
            
            x = rowMean.keys().to_list()
            y = rowMean.to_list()
            y_err = rowStd.to_list()

            # ax.bar(x, y, yerr = y_err)
            boxdata.boxplot(ax = ax, showmeans = True)
            ax.tick_params(axis = 'x', rotation = 45)

            box_max = max(boxdata.max().to_list())
            if  box_max <= 1:
                box_max = 1
            
            ax.set_ylim(0, box_max) 
            
    fig.show()


# Main
root = '..\\data\\results\\'
segments = ['brain', 'brainstem', 'spinalcord', 'parotid_merged']
segments = ['pcm_low', 'pcm_mid', 'pcm_up']
metrics = ['DICE', 'Hausdorff', 'EPL', 'EPL_L', 'EPL_V', 'MSD']
comparisons = ['GTvsDL', 'GTvsDLB']

for tolerance in {0, 1, 2}:
    raw = pd.read_csv(root + f'total_tolerance{tolerance}.csv')
    temp = pd.concat([raw.iloc[:, 2:4], raw[segments]], axis = 1)
    temp = temp[temp.Comparison.isin(comparisons)]
    temp = temp[temp.Metric.isin(metrics)]
    total = temp
    # print(total)

    new = total[total.Comparison == 'GTvsDL']
    new = new[new.Metric == 'DICE']
    # print(new.iloc[:, 2:])


    test = total.groupby(by = ['Comparison', 'Metric']).mean()

    myFig(total, title = f'Tolerance {tolerance}')


