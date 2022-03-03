"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: Main.py

Discribtion:
"""

# # Imports
import os
import SimpleITK as ITK
import numpy as np

# # Import other files
# Classes
from DataReader import datareader
from DataPreparation import OAR

# Functions
from DICE import DICE
from Hausdorff import Hausdorff
# from MeanSurfaceDistance import Mean

# # Classes and functions
def PatientGenerator(n):
    dir = "A:\\data\\GT"
    for file in os.listdir(dir)[:n]:
        PatientID = file.split("&")[0]
        yield PatientID

# # Run file (optional)
for Patient in PatientGenerator(10):
    print(Patient)

    



