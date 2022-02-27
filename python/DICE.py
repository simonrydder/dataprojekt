"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: DICE.py

Discription:

Python script to calculate the DICE coefficient between two surfaces. 
"""

# Imports
import os
import SimpleITK as ITK
import numpy as np

# Import other files


# Classes and functions
def DICE(P1, P2):
    assert isinstance(P1, )
    assert isinstance(P2, )
    
    Dice_list = list()
    Jaccard_list = list()  
    quality = dict()

    labelPred = ITK.GetArrayFromImage(P1, isVector=False)
    labelTrue = ITK.GetArrayFromImage(P2, isVector=False)

    dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
    dicecomputer.Execute(labelTrue>0.5,labelPred>0.5)
    quality["dice"]=dicecomputer.GetDiceCoefficient()
    quality["jaccard"]=dicecomputer.GetJaccardCoefficient()

    Dice_list.append(quality["dice"])
    Jaccard_list.append(quality["jaccard"]

    return quality

# Run file (optional)



