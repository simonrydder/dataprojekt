"""
Authors: Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created: 21/02/2022

File name: Main.py

Discribtion: 
"""

# Imports
import os
import SimpleITK as ITK
import numpy as np

# # Import other files
# Classes
from DataReader import Path
from DataPreparation import OAR_Image
from eskildmetric import Metrics

# Functions
#from DICE import DICE
#from Hausdorff import Hausdorff
# from MeanSurfaceDistance import Mean

# # Classes and functions
def PatientGenerator(n = "All"):
    dir = "A:\\data\\GT"
    if isinstance(n, int):
        for file in os.listdir(dir)[:n]:
            PatientID = file.split("&")[0]
            yield PatientID
    else:
        for file in os.listdir(dir):
            PatientID = file.split("&")[0]
            yield PatientID

# # Run file (optional)
# Segment = "BrainStem"
# Methods = ["GT", "DL", "DLB"]
# for Patient in PatientGenerator(100):
#     MET = Metrics(Patient, Segment, Methods)
#     print(MET)



# # # Run file (optional)
# Segment = "BrainStem"
# Methods = ["GT", "DL", "DLB"]
# for Patient in PatientGenerator(10):
#     L.append(Patient)

# for Patient in L:
#     MET = Metrics(Patient, Segment, Methods)
#     print(MET)



