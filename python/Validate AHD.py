"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Validate.py

Discribtion:    Check SimpleITK's HaussdorffDistanceImageFilter computes the Average Surface Distance
"""


import numpy as np
import SimpleITK as ITK

A1 = np.array([[0,0,0,0,0],
             [0,1,1,1,0],
             [0,1,1,1,0],
             [0,1,1,1,0],
             [0,0,0,0,0]])

B1 = np.array([[0,0,0,0,0],
             [0,0,1,1,1],
             [0,0,1,1,1],
             [0,0,1,1,1],
             [0,0,0,0,0]])

A2 = np.array([[0,0,0,0,0],
             [0,1,1,1,0],
             [0,1,1,1,0],
             [0,1,1,1,0],
             [0,0,1,0,0]])

B2 = np.array([[0,0,0,0,0],
             [0,0,1,1,1],
             [0,0,1,1,1],
             [0,0,1,1,1],
             [0,0,0,0,0]])

A1_image = ITK.GetImageFromArray(A1)

B1_image = ITK.GetImageFromArray(B1)


A2_image = ITK.GetImageFromArray(A2)

B2_image = ITK.GetImageFromArray(B2)


Comp = ITK.HausdorffDistanceImageFilter()

Comp.Execute(A1_image > 0.5,B1_image > 0.5)

Comp.GetAverageHausdorffDistance() #(1/3+1/3)/2 = 1/3
 
Comp.Execute(A2_image > 0.5,B2_image > 0.5)

Comp.GetAverageHausdorffDistance() #(2/5+1/3)/2= 0.3667