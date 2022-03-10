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
        self.Hausdorff  = self.getHausdorff()     # Dictionary 
        self.MSD        = self.getMSD() # Dictionary
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
        
        for met1, met2 in self.comparisons:
            P1 = getattr(self, met1).Image
            P2 = getattr(self, met2).Image

            dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
            dicecomputer.Execute(P2>0.5,P1>0.5)
            DICE_dict[(met1, met2)]=dicecomputer.GetDiceCoefficient()
        
        return DICE_dict

    def getHausdorff(self):
        Haus_dict = {}

        for i, comp in enumerate(self.comparisons):
            Haus_dict[comp] = "None" + str(i)
        
        for met1, met2 in self.comparisons:
            P1 = getattr(self, met1).Image
            P2 = getattr(self, met2).Image

            hauscomputer = ITK.HausdorffDistanceImageFilter()
            hauscomputer.Execute(P2>0.5,P1>0.5)
            Haus_dict[(met1, met2)]=hauscomputer.GetHausdorffDistance()
        
        return Haus_dict

    def getMSD(self):
        MSD_dict = {}
        for i, comp in enumerate(self.comparisons):
            MSD_dict[comp] = "None" + str(i)
        
        for met1, met2 in self.comparisons:
            P1 = getattr(self, met1).Image
            P2 = getattr(self, met2).Image

            MSDcomputer = ITK.HausdorffDistanceImageFilter()
            MSDcomputer.Execute(P2>0.5,P1>0.5)
            MSD_dict[(met1, met2)]=MSDcomputer.GetAverageHausdorffDistance()
        
        
        return MSD_dict

    def getAPL(self):
        pass



# Test
PatientID = "1cbDrFdyzAXjFICMJ58Hmja9U"
#Segment = "BrainStem"
Segment = "mandible" 
Methods = ["GT", "DL", "DLB"]

print(Path(PatientID, Methods[0]).File)

MET = Metrics(PatientID, Segment, Methods)
print(MET)
