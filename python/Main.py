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
import pandas as pd
from pyparsing import col

# # Import other files
# Classes
from Metrics import Metrics

# Functions

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
# Methods = ["GT", "DL"]
# print("\nTEST FROM THIS FILE:")
# for Patient in PatientGenerator(5):
#     MET = Metrics(Patient, Segment, *Methods)
#     print(MET)
#     print()

# # Main loop
data = {'ID': [],
        'Date' : [],
        'Metric': [],
        'Comparison':[]}

print(data)

for i, Segment in enumerate(['brainstem', 'parotid_merged']):
    data[Segment] = []
    for Comparisons in [('GT', 'DL'), ('GT', 'DLB')]:
        for Patient in PatientGenerator(10):
            Metric = Metrics(Patient, Segment, *Comparisons)
            for value in ['DICE', 'Hausdorff', 'MSD', 'APL', 'APL_length_ratio', 'APL_volume_ratio']:

                if i == 0:
                    data['ID'].append(Metric.PatientID)
                    data['Date'].append(Metric.ImageA.Date)
                    data['Comparison'].append(Metric.Comparison)
                    data['Metric'].append(value)
                
                data[Segment].append(getattr(Metric, value))

# number of rows = number of patients * number of methods

df = pd.DataFrame(data, columns = data.keys())
df.to_csv('test.csv')

# # # Run file (optional)
# Segment = "BrainStem"
# Methods = ["GT", "DL", "DLB"]
# for Patient in PatientGenerator(10):
#     L.append(Patient)

# for Patient in L:
#     MET = Metrics(Patient, Segment, Methods)
#     print(MET)



