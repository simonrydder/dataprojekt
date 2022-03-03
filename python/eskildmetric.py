"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Metrics.py

Discribtion:    Skabelon for nye filer.
"""

# Imports
from math import comb
import os
import SimpleITK as ITK

# Import other files
from DataReader import Path
from DataPreparation import OAR_Image
# from DICE import DICE

# Classes and functions
class Metrics():
    def __init__(self, ID, segment, methods):
        self.PatientID = ID     # As id-type
        self.OAR = segment      # As string i.e. "Brainstem"
        for method in methods:
            setattr(self, method, self.getImage(method))
        self.comparisons = [(M1, M2,) for M1 in methods for M2 in methods if M1 < M2]
        self.DICE       = self.getDICE()     # Dictionary
        self.Hausdorff  = self.getDICE()     # Dictionary 
        self.MSD        = self.getDICE() # Dictionary
        self.APL        = self.getDICE() # Dictionary

    def __str__(self):
        MetricPrint =   f'PatientID: {self.PatientID}\n' + \
                        f'OAR: {self.OAR}\n' + \
                        f'DICE: {self.DICE}\n' + \
                        f'Hausdorff: {self.Hausdorff}\n' + \
                        f'Mean Surface Distance: {self.MSD}\n' + \
                        f'Added Path Length (Ratio): {self.APL}'
        
        return MetricPrint

    def getImage(self, method):
        File = Path(self.PatientID, method).File
        image = OAR_Image(File, self.OAR)
        return image
    
    def getDICE(self):
        DICE_dict = {}
        for i, comp in enumerate(self.comparisons):
            DICE_dict[comp] = "None" + str(i)
        
        for comb in self.comparisons:
            met1, met2 = comb
            P1, P2 = self.getImage(met1).GetImage(), self.getImage(met2).GetImage()
            #Compute overlap measurements:
            dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
            dicecomputer.Execute(P2>0.5,P1>0.5)
            DICE_dict[comb]=dicecomputer.GetDiceCoefficient()
        
        return DICE_dict

    def getHausdorff(self):
        # Same priciple as getDICE() 
        return None

# Test
PatientID = "1cbDrFdyzAXjFICMJ58Hmja9U"
Segment = "BrainStem"
Methods = ["GT", "DL", "DLB"]

print(Path(PatientID, Methods[0]).File)

MET = Metrics(PatientID, Segment, Methods)
print(MET)

for m in L:
    P1, P2 = m