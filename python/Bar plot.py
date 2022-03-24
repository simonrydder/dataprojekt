"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      skabelon.py

Discribtion:    Skabelon for nye filer.
"""

# Imports

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv("test.csv", index_col = 0)
df = df.drop(["Date"], axis = 1).round(2)


def bar_plot(df):
    metrics = df["Metric"].unique().tolist()
    df_sliced_dict = {}

    for metric in metrics:
        df_sliced_dict[metric] = df[df['Metric'] == metric]
    
    nrow = 2; ncol = 3
    fig, axs = plt.subplots(nrows=nrow, ncols=ncol)
    fig.tight_layout(rect=[0, 0.03, 1, 0.9])
    plt.suptitle("Performance for 5 patients", fontsize=20)
    sns.set_theme(style="whitegrid")
    titles = {"DICE": "Dice Coeffienct", "Hausdorff": "Max Hausdorff distance", "MSD": "Mean Surface Distance",
                "APL": "Added Path Length in MM", "APL_length_ratio": "APL divide by complete path length", 
                "APL_volume_ratio": "APL divide by complete volume"}

    for idx,ax in enumerate(axs.reshape(-1)): 
        try:
            df_means = df_sliced_dict[metrics[idx]].groupby(["Comparison"]).mean()
            df_means.plot(ax=ax, kind='bar', rot = 0, legend = 0)    
            ax.set_title(label = titles.get(metrics[idx]), fontsize = 15)
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set(xlabel =None)
            if metrics[idx] not in ['APL', 'Hausdorff']:
                ax.set_ylim(0,1)
        except IndexError:
            break
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right',prop={'size': 18})
    plt.show()


bar_plot(df)



