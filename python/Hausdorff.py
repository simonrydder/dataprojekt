"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: Hausdorff.py

Discription:

Python script to calculate the Hausdorff Distance between two surfaces. 
"""

# Imports
import os
import SimpleITK as ITK
import numpy as np

# Import other files


# Classes and functions
def Hausdorff(P1, P2):
    assert isinstance(P1, )
    assert isinstance(P2, )

    AvgHausdorff_list = list()
    Hausdorff_list = list()

    labelPred = ITK.GetImageFromArray(P1, isVector=False)
    labelTrue = ITK.GetImageFromArray(P2, isVector=False)
    
    hausdorffcomputer = ITK.HausdorffDistanceImageFilter()
    hausdorffcomputer.Execute(labelTrue>0.5,labelPred>0.5)

    quality["avgHausdorff"]=hausdorffcomputer.GetAverageHausdorffDistance()
    quality["Hausdorff"]=hausdorffcomputer.GetHausdorffDistance()

    AvgHausdorff_list.append(quality["avgHausdorff"])
    Hausdorff_list.append(quality["Hausdorff"])

    return quality

# Run file (optional)



