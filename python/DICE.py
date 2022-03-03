"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: DICE.py

Discription:

Python script to calculate the DICE coefficient between the same set of labels of pixels of two images P1, P2. Background is assumed to be 0.
"""

# Imports
import os
import SimpleITK as ITK
import numpy as np
import DataReader
import DataPreparation

# Import other files


# Classes and functions
def DICE(P1, P2):

    #Input must be of type ITK.Image:
    assert isinstance(P1, ITK.SimpleITK.Image), "Error input P1 is not a valid ITK.Image type"
    assert isinstance(P2, ITK.SimpleITK.Image), "Error input P2 is not a valid ITK.Image type"


    #Save results in list and append to dictionary
    Dice_list = list()
    Jaccard_list = list()  
    quality = dict()


    #Compute overlap measurements:
    dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
    dicecomputer.Execute(P2>0.5,P1>0.5)
    quality["dice"]=dicecomputer.GetDiceCoefficient()
    quality["jaccard"]=dicecomputer.GetJaccardCoefficient()

    Dice_list.append(quality["dice"])
    Jaccard_list.append(quality["jaccard"])

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

DICE(P1, P2)



