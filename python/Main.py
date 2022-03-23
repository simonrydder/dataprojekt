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

# # Import other files
# Classes
from Metrics import Metrics_Info

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

def PatientKeys(n = "All"):
    dir = "A:\\data\\GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys

test1 = {'Patients' : PatientKeys(5),
         'Segments' : {'brainstem', 'spinalcord'},
         'Comparisons' : {('GT', 'DL'), ('GT', 'DLB')},
         'Metrics' : {'DICE', 'MSD', 'ALP_lenght_ratio'}}

file = 'brainstem&GTvsDL&DICE'

test2 = {'Patients' : PatientKeys(5),
         'Segments' : {'brainstem', 'parotid_merged'},
         'Comparisons' : {('GT', 'DL'), ('GT', 'DLB')},
         'Metrics' : {'DICE', 'MSD', 'ALP_lenght_ratio'}}

test3 = {'Patients' : PatientKeys(10),
         'Segments' : {'brainstem', 'parotid_merged'},
         'Comparisons' : {('GT', 'DL'), ('GT', 'DLB')},
         'Metrics' : {'DICE', 'Hausdorff', 'ALP_lenght_ratio'}}

# class MyException(Exception):
#     pass

# try:
#     if True:
#         raise MyException
    
# except MyException:
#     #create NA

def func(file, Patients, Segments, Comparisons, Metrics, overwrite = False):
    try:
        if overwrite:
            raise FileNotFoundError
        cur = pd.read_csv('test.csv')
    except FileNotFoundError:
        cur = pd.DataFrame({'ID': [],
                            'Date' : [],
                            'Comparison': [],
                            'Metric':[]})

    cols = cur.columns

    c_Patients = {(ID, Date) for ID, Date in cur[cols[:2]].values}
    c_Segments = {seg for seg in cols[4:]}
    comps = [c.split() for c in cur[cols[3]]]
    c_Comparisons = {(first, second) for first, _, second in comps}
    c_Metrics = {Metric for Metric in cur[cols[2]]}
    
    
    
    return key

print(func('test.csv', *test1.values()))

test = pd.read_csv('test.csv')
x = test.groupby(["ID", "Date"])
key, cols = test.columns[:4], test.columns[4:]
x = {(ID, Date) for ID, Date in test[key[:2]].values}
print(x)
y = list(x)
print(y)
for x, y in test[key[:2]].values:
    print(type(y))
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
            MI = Metrics_Info(Patient, Segment, *Comparisons)
            for Metric in ['DICE', 'Hausdorff', 'MSD', 'APL', 'APL_length_ratio', 'APL_volume_ratio']:

                if i == 0:
                    data['ID'].append(MI.PatientID)
                    data['Date'].append(MI.ImageA.Date)
                    data['Comparison'].append(MI.Comparison)
                    data['Metric'].append(Metric)
                
                data[Segment].append(getattr(MI, Metric))

# number of rows = number of patients * number of methods

df = pd.DataFrame(data, columns = data.keys())
df.to_csv('test.csv', index=False)

# # # Run file (optional)
# Segment = "BrainStem"
# Methods = ["GT", "DL", "DLB"]
# for Patient in PatientGenerator(10):
#     L.append(Patient)

# for Patient in L:
#     MET = Metrics(Patient, Segment, Methods)
#     print(MET)



