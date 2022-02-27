"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: Hausdorff.py

Discription:

Python script to calculate the Hausdorff Distance between the same set of labels consisting of pixels from two images P1, P2. Background is assumed to be 0 
"""

# Imports
import os
import SimpleITK as ITK
import numpy as np
import DataReader
import DataPreparation

# Import other files


# Classes and functions
def Hausdorff(P1, P2):

    #Input must be of type ITK.Image:
    assert isinstance(P1, ITK.SimpleITK.Image)
    assert isinstance(P2, ITK.SimpleITK.Image)


    #Save results in list and append to dictionary
    AvgHausdorff_list = list()
    Hausdorff_list = list()
    quality = dict()


    #Compute overlap measurements:
    hausdorffcomputer = ITK.HausdorffDistanceImageFilter()
    hausdorffcomputer.Execute(P2>0.5,P1>0.5)

    quality["avgHausdorff"]=hausdorffcomputer.GetAverageHausdorffDistance()
    quality["Hausdorff"]=hausdorffcomputer.GetHausdorffDistance()

    AvgHausdorff_list.append(quality["avgHausdorff"])
    Hausdorff_list.append(quality["Hausdorff"])

    return quality

# Run file (optional)

ID = "1cbDrFdyzAXjFICMJ58Hmja9U"     

x = DataReader.datareader(ID)
P1 = x.DL
P2 = x.GT
segment = 'BraiNSteM'

P1 = DataPreparation.OAR(P1, segment)
P2 = DataPreparation.OAR(P2, segment)

P1 = P1.GetImage()
P2 = P2.GetImage()

Hausdorff(P1, P2)

