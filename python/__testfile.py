
import os
import numpy as np
from Metrics import Metrics_Info
from DataReader import Path
from DataPreparation import OAR_Image

def PatientKeys(n = "All"):
    dir = "A:\\data\\GT"
    files = os.listdir(dir)
    if isinstance(n, int):
        files = files[:n]
    keys = {(ID, Date[:8]) for ID, Date in [file.split('&') for file in files]}

    return keys

Patients = list(PatientKeys(1))[0]

GT = Path(*Patients, Method = 'GT')
DL = Path(*Patients, Method = 'DL')

OARGT = OAR_Image(GT, 'brainstem')
OARDL = OAR_Image(DL, 'brainstem')
space = np.array(OARGT.Spacing)

MI = Metrics_Info(OARGT, OARDL)
print(MI)

A = OARGT.GetArray()
B = OARDL.GetArray()

min_distances = []
for z0, y0, x0 in zip(*A.nonzero()):
    a = np.array((x0, y0, z0))

    min_dist = 10000
    for z1, y1, x1 in zip(*B.nonzero()):
        b = np.array((x1, y1, z1))

        dist = np.linalg.norm((a - b)*space)
        min_dist = dist if dist < min_dist else min_dist
    
    min_distances.append(min_dist)
    if len(min_distances) % 50 == 0:
        print(len(min_distances))

print(max(min_distances))
