"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      ValidateMatrices.py

Discribtion:    This file is a visual check of the implemented 
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pandas as pd
import seaborn as sns
import SimpleITK as ITK

# Import other files
from DataPreparation import OAR_Image
from DataReader import Path

# Classes and functions

def findCoordinates(array):
    """
    Input:  An array A[y][x]
    Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] == 1.
    """
    N = len(array)
    coords = np.where(array > 0)
    return [(x + 1, N - y) for y, x in zip(*coords)]


def findLines(coordinates):
    """
    Input:  A list of coordinates for the center of a pixel.
    Outout: Two lists of linesegments. One for horizontal linesegments and one for vertical linesegments.
    """

    verticals = {}
    horizontals = {}

    for x, y in coordinates:
        left = ((x - 0.5, y - 0.5), (x - 0.5, y + 0.5)) # left edge line
        right = ((x + 0.5, y - 0.5), (x + 0.5, y + 0.5)) # right edge line
        lower = ((x - 0.5, y - 0.5), (x + 0.5, y - 0.5)) # lower edge line
        upper = ((x - 0.5, y + 0.5), (x + 0.5, y + 0.5)) # upper edge line

        for line in left, right, lower, upper:
            (x0, _), (x1, _) = line
            if x0 == x1: # vertical line
                verticals[line] = verticals.get(line, 0) + 1
            else: # horizontal line
                horizontals[line] = horizontals.get(line, 0) + 1 
    
    # Extraxt only lines not dublicating.
    Vlines = [key for key, value in verticals.items() if value == 1]
    Hlines = [key for key, value in horizontals.items() if value == 1]
    
    return Vlines, Hlines


def findLimits(x, y, limits = []):
    Xmin = min(x) - 1
    Xmax = max(x) + 1
    Ymin = min(y) - 1
    Ymax = max(y) + 1
    
    if limits != []:
        Xmin = min(Xmin, limits[0][0])
        Xmax = max(Xmax, limits[0][1])
        Ymin = min(Ymin, limits[1][0])
        Ymax = max(Ymax, limits[1][1])

    return [(Xmin, Xmax), (Ymin, Ymax)]


def metrics_slice(patient,method,segment,i):
    pathA = Path(patient, "GT")
    OAR_A = OAR_Image(pathA.File, segment)
    array_A = OAR_A.GetArray()
    array_A = array_A[i]
    img_A = ITK.GetImageFromArray(array_A)

    pathB = Path(patient, method)
    OAR_B = OAR_Image(pathB.File, segment)
    array_B = OAR_B.GetArray()
    array_B = array_B[i]
    img_B = ITK.GetImageFromArray(array_B)


    hauscomputer = ITK.HausdorffDistanceImageFilter()
    hauscomputer.Execute(img_A>0.5,img_B>0.5)

    MSDcomputer = ITK.HausdorffDistanceImageFilter()
    MSDcomputer.Execute(img_A>0.5,img_B>0.5)

    dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
    dicecomputer.Execute(img_A>0.5,img_B>0.5) 

    return np.round(hauscomputer.GetHausdorffDistance(),3), \
            np.round(MSDcomputer.GetAverageHausdorffDistance(),3), \
            np.round(dicecomputer.GetDiceCoefficient(),3)
    

def Organ_plot(ax,patient,segment,method,title):
    pathA = Path(patient, "GT")
    pathB = Path(patient, method)

    OAR_A = OAR_Image(pathA.File, segment)
    OAR_B = OAR_Image(pathB.File, segment)

    A = OAR_A.GetArray()
    B = OAR_B.GetArray()

    for z in range(A.shape[0]):
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_min = z
            break

    for z in range(A.shape[0])[::-1]:
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_max = z
            break

    i = (z_max - z_min)//2 + z_min - 5

    A = A[i]
    B = B[i]
    ax.set_title(title)

    # Plotting A
    coordsA = findCoordinates(A)
    x, y = zip(*coordsA)
    limits = findLimits(x, y)
    ax.plot(x, y, color = 'b', marker = 'o', ls = '', label = "A (Truth): Pixels")

    VA, HA = findLines(coordsA)

    Legend = "A (Truth): Drawn line"
    for line in VA:
        (x, y0), (_, y1) = line
        ax.vlines(x, ymin = y0, ymax = y1, colors = 'b', linestyles = 'dashdot', label = Legend)
        Legend = '_nolegend_'

    for line in HA:
        (x0, y), (x1, _) = line
        ax.hlines(y, xmin = x0, xmax = x1, colors = 'b', linestyles = 'dashdot', label = '_nolegend_')

    # Plotting B
    coordsB = findCoordinates(B)
    x, y = zip(*coordsB)
    limits = findLimits(x, y, limits)
    ax.plot(x, y, color = 'r', marker = '.', ls = '', label = "B (Guess): Pixels")

    VB, HB = findLines(coordsB)

    Legend = "B (Guess): Drawn line"
    for line in VB:
        (x, y0), (_, y1) = line
        ax.vlines(x, ymin = y0, ymax = y1, colors = 'r', linestyles = 'dashed', label = Legend)
        Legend = '_nolegend_'

    for line in HB:
        (x0, y), (x1, _) = line
        ax.hlines(y, xmin = x0, xmax = x1, colors = 'r', linestyles = 'dashed',
                                        label = '_nolegend_')

    Vrest = set(VA) - set(VB)
    Hrest = set(HA) - set(HB)
    value = np.round(len(Vrest)*OAR_A.Spacing[1] + 
                        len(Hrest)*OAR_A.Spacing[0],2)
    length = len(VA)*OAR_A.Spacing[1] + len(HA)*OAR_A.Spacing[0]
    volume = (OAR_A.Spacing[1] + OAR_A.Spacing[0]) * len(coordsA)
    
    APL_length = np.round(value/length,3)
    APL_volume = np.round(value/volume,3)

    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.yaxis.set_label_position("right")

    haus, MSD, DICE = metrics_slice(patient,method,segment,i)

    metrics_string = "\n".join((f'APL: {value} mm | APL_length: {APL_length} | APL_volume:{APL_volume}',
                        f'Dice: {DICE} | Hausdorff: {haus} | MSD: {MSD}'))

    props = dict(boxstyle='round', facecolor='grey', alpha=0.5)
                    
    ax.set_xlabel(metrics_string, fontsize=10,
                  loc='center',bbox=props, rotation = 0)
    ax.set_aspect("equal")             
    ax.set_anchor("C")









# read data in
df = pd.read_csv("test.csv", index_col = 0)
patients = df["ID"].unique().tolist()


def plot(segments,methods,patients):
    nrow = 3
    ncol = 3
    for segment in segments:
        for method in methods:
            dimensions = []
            idx = 0
            fig, axs = plt.subplots(nrows=nrow, ncols=ncol)
            plt.subplots_adjust(hspace=0.4)
            plt.suptitle(f"{segment} for {method}", fontsize = 25)
            for row in range(nrow):
                for col in range(ncol):
                    idx += 1
                    Organ_plot(axs[row,col],patients[idx],segment,method, 
                                                    f"patient {idx}")

        
            handles, labels = axs[row,col].get_legend_handles_labels()
            fig.legend(handles, labels, 
                loc="upper right",prop={'size': 11})


    plt.show()


segments = ["brainstem", "parotid_merged"]
methods = ["DL", "DLB"]

plot(segments,methods,patients)

