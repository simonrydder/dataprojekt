"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      ValidateMatrices.py

Discribtion:    This file is for creating csv files to dash app (meanwhile)
"""

# Imports
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import pandas as pd
import SimpleITK as ITK
import os

# Import other files
from DataPreparation import OAR_Image
from DataReader import Path

# Classes and functions

def findCoordinates(array):
    """
    Input:  An array A[y][x]
    Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] == 1.
    """
    N = len(array)
    coords = np.where(array > 0)
    if len([(x + 1, N - y) for y, x in zip(*coords)]) == 0:
        return []
    else:
        return [(x + 1, N - y) for y, x in zip(*coords)]



def findLines(coordinates):
    """
    Input:  A list of coordinates for the center of a pixel.
    Outout: Two lists of linesegments. One for horizontal linesegments and one for vertical linesegments.
    """

    verticals = {}
    horizontals = {}

    for x, y in coordinates:
        left = ((x - 0.5, y - 0.5), (x - 0.5, y + 0.5)) # left edge line
        right = ((x + 0.5, y - 0.5), (x + 0.5, y + 0.5)) # right edge line
        lower = ((x - 0.5, y - 0.5), (x + 0.5, y - 0.5)) # lower edge line
        upper = ((x - 0.5, y + 0.5), (x + 0.5, y + 0.5)) # upper edge line

        for line in left, right, lower, upper:
            (x0, _), (x1, _) = line
            if x0 == x1: # vertical line
                verticals[line] = verticals.get(line, 0) + 1
            else: # horizontal line
                horizontals[line] = horizontals.get(line, 0) + 1 
    
    # Extraxt only lines not dublicating.
    Vlines = [key for key, value in verticals.items() if value == 1]
    Hlines = [key for key, value in horizontals.items() if value == 1]
    
    return Vlines, Hlines

def metrics_slice(patient,method,segment,i):
    m1, m2 = method
    pathA = Path(patient, m1)
    OAR_A = OAR_Image(pathA.File, segment)
    array_A = OAR_A.GetArray()
    array_A = array_A[i]
    img_A = ITK.GetImageFromArray(array_A)

    pathB = Path(patient, m2)
    OAR_B = OAR_Image(pathB.File, segment)
    array_B = OAR_B.GetArray()
    array_B = array_B[i]
    img_B = ITK.GetImageFromArray(array_B)


    hauscomputer = ITK.HausdorffDistanceImageFilter()
    hauscomputer.Execute(img_A>0.5,img_B>0.5)

    MSDcomputer = ITK.HausdorffDistanceImageFilter()
    MSDcomputer.Execute(img_A>0.5,img_B>0.5)

    dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
    dicecomputer.Execute(img_A>0.5,img_B>0.5) 

    return np.round(hauscomputer.GetHausdorffDistance(),3), \
            np.round(MSDcomputer.GetAverageHausdorffDistance(),3), \
            np.round(dicecomputer.GetDiceCoefficient(),3)
 
    
def findlimits(A,B):
    _,yA,xA = np.where(A>0)
    _,yB,xB = np.where(B>0)

    min_y = min(list(yA)+list(yB))
    max_y = max(list(yA)+list(yB))
    min_x = min(list(xA)+list(xB))
    max_x = max(list(xA)+list(xB))

    return min_x, max_x, min_y, max_y


def findslice(patient, method, segment):

    pathA = Path(patient, "GT")
    pathB = Path(patient, method)

    OAR_A = OAR_Image(pathA.File, segment)
    OAR_B = OAR_Image(pathB.File, segment)

    A = OAR_A.GetArray()
    B = OAR_B.GetArray()

    if np.sum(A) == 0:
        return None

    for z in range(A.shape[0]):
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_min = z
            break

    for z in range(A.shape[0])[::-1]:
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_max = z
            break
    
    i = (z_max - z_min)//2 + z_min
    idx = 0
    ranthrough = False
    while True:
        if np.sum(A[i,:,:]) == 0 or np.sum(B[i,:,:]) == 0:
            i += 1
            if i == z_max and not ranthrough:
                ranthrough=True
                i = z_min
            if i > z_max and ranthrough:
                return None
        else:
            break

    coordsA = findCoordinates(A[i])
    xA, yA = zip(*coordsA)
    VA, HA = findLines(coordsA)
    coordsB = findCoordinates(B[i])
    xB, yB = zip(*coordsB)
    VB, HB = findLines(coordsB)


    return patient, segment, list(xA), list(yA), list(xB), list(yB), VA, HA, VB, HB


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

segments = ["brainstem", "spinalcord",
"lips", "esophagus", "parotid_merged", "pcm_low",
"pcm_mid", "pcm_up", "mandible", "submandibular_merged",
"thyroid", "opticNerve_merged", "eyefront_merged"]
patients = PatientGenerator() 
methods = ["DL"]
data = {"Patient": [], "Segment": [],
        "xA": [], "yA": [],
        "xB":[] , "yB": [],"VA": [],"HA": [],"VB": [],"HB": []}
    
for patient in patients:
    print(patient)
    for segment in segments:
        for method in methods:
            #Patient, Segment, xA, yA, xB, yB = findslice(patient,method,segment)
            data_patient = findslice(patient,method,segment)
            if data_patient != None:
                for key, value in zip(data.keys(),data_patient):
                    data[key].append(value)

df = pd.DataFrame(data)
df.to_csv("data_organ_test.csv")


patients = list(PatientGenerator(2))
segments = [ "brainstem", "spinalcord",
"lips", "esophagus", "parotid_merged"]
method = "DL"

def findslice2(patients, method, segments):

    data = {"Patient": [], "Segment": [],"method": [],"idx": [],"slice": [],
        "xA": [], "yA": [], "xB":[] , "yB": [],"VA": [],"HA": [],
        "VB": [],"HB": [], 
        "APL": [],"APL_L": [], "APL_V": [], "DICE": [], "MSD": [],
         "Hausdorff": []}
    
    for patient in patients:
        print(patient)
        for segment in segments:
            print(segment)

            pathA = Path(patient, "GT")
            pathB = Path(patient, method)

            OAR_A = OAR_Image(pathA.File, segment)
            OAR_B = OAR_Image(pathB.File, segment)

            A = OAR_A.GetArray()
            B = OAR_B.GetArray()

            if np.sum(A) == 0:
                return None

            for z in range(A.shape[0]):
                if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
                    z_min = z
                    break

            for z in range(A.shape[0])[::-1]:
                if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
                    z_max = z
                    break 
            

            for idx,z in enumerate(range(z_min,z_max+1)):
                coordsA = findCoordinates(A[z])
                both = True
                if len(coordsA)  == 0:
                    xA = []
                    yA = []
                    VA = []
                    HA = []
                    both = False
                else:
                    xA, yA = zip(*coordsA)
                    VA, HA = findLines(coordsA)
    
                coordsB = findCoordinates(B[z])
                if len(coordsB) == 0:
                    xB = []
                    yB = []
                    VB = []
                    HB = []
                    both = False
                else:
                    xB, yB = zip(*coordsB)
                    VB, HB = findLines(coordsB)
                

                if both:
                    Hausdorff, MSD, DICE = metrics_slice(patient,method,segment,z)
                    Vrest = set(VA) - set(VB)
                    Hrest = set(HA) - set(HB)
                    APL = np.round(len(Vrest)*OAR_A.Spacing[1] + 
                                len(Hrest)*OAR_A.Spacing[0],2)
                    length = len(VA)*OAR_A.Spacing[1] + len(HA)*OAR_A.Spacing[0]
                    volume = (OAR_A.Spacing[1] + OAR_A.Spacing[0]) * len(coordsA)
            
                    APL_length = np.round(APL/length,3)
                    APL_volume = np.round(APL/volume,3)

                else:
                    Hausdorff = None
                    MSD = None
                    DICE = None
                    APL = None
                    APL_length = None
                    APL_volume = None

               

                data_slice = [patient,segment,idx,z,list(xA),list(yA),list(xB),
                                list(yB),VA,HA,VB,HB,
                                APL,APL_length, APL_volume,DICE, MSD, Hausdorff]


                for key, value in zip(data.keys(),data_slice):
                            data[key].append(value)

            



    return data

data = findslice2(patients,method,segments)
df = pd.DataFrame(data)

df.to_csv("data_slices_test.csv")




patients = ["4Prj3A5sMvSv1sK4u5ihkzlnU"]
methods = [("GT","DL"),("GT","DLB"),("DL","DLB")]
segments = ["brain","brainstem", "spinalcord",
"lips", "esophagus", "parotid_merged", "pcm_low",
"pcm_mid", "pcm_up", "mandible", "submandibular_merged",
"thyroid", "opticNerve_merged", "eyefront_merged"]


data = {"Patient": [], "Segment": [],"method": [],"idx": [],"slice": [], "xA":[] , "yA": [],
"xB": [],"yB": [], "VA": [],"HA": [],"VB": [],"HB": [],
"APL": [],"APL_L": [], "APL_V": [], "DICE": [], "MSD": [],
"Hausdorff": []}
for patient in patients:
    print(patient)
    for method in methods:
        m1, m2 = method
        print(method)
        for segment in segments:
            print(segment)

            pathA = Path(patient, m1)
            pathB = Path(patient, m2)

            OAR_A = OAR_Image(pathA.File, segment)
            OAR_B = OAR_Image(pathB.File, segment)

            A = OAR_A.GetArray()
            B = OAR_B.GetArray()

            if np.sum(A) != 0:

                for z in range(A.shape[0]):
                    if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
                        z_min = z
                        break

                for z in range(A.shape[0])[::-1]:
                    if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
                        z_max = z
                        break 


                for idx,z in enumerate(range(z_min,z_max+1)):
                    coordsA = findCoordinates(A[z])
                    both = True
                    if len(coordsA)  == 0:
                        xA = []
                        yA = []
                        VA = []
                        HA = []
                        both = False
                    else:
                        xA, yA = zip(*coordsA)
                        VA, HA = findLines(coordsA)

                    coordsB = findCoordinates(B[z])
                    if len(coordsB) == 0:
                        xB = []
                        yB = []
                        VB = []
                        HB = []
                        both = False
                    else:
                        xB, yB = zip(*coordsB)
                        VB, HB = findLines(coordsB)


                    if both:
                        Hausdorff, MSD, DICE = metrics_slice(patient,method,segment,z)
                        Vrest = set(VA) - set(VB)
                        Hrest = set(HA) - set(HB)
                        APL = np.round(len(Vrest)*OAR_A.Spacing[1] + 
                                    len(Hrest)*OAR_A.Spacing[0],2)
                        length = len(VA)*OAR_A.Spacing[1] + len(HA)*OAR_A.Spacing[0]
                        volume = (OAR_A.Spacing[1] + OAR_A.Spacing[0]) * len(coordsA)

                        APL_length = np.round(APL/length,3)
                        APL_volume = np.round(APL/volume,3)

                    else:
                        Hausdorff = None
                        MSD = None
                        DICE = None
                        APL = None
                        APL_length = None
                        APL_volume = None



                    data_slice = [patient,segment,method,idx,z,xA,yA,xB,yB,VA,HA,VB,HB,
                                    APL,APL_length, APL_volume,DICE, MSD, Hausdorff]


                    for key, value in zip(data.keys(),data_slice):
                                data[key].append(value)



    df = pd.DataFrame(data)
    name = patient + "_test.csv"
    df.to_csv(name)