"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Metrics.py

Discription:    Metrics class to perform all metrics relevant to project.
"""

# Imports
from math import comb
import os
import SimpleITK as ITK

# Import other files
from DataReader import Path
from DataPreparation import OAR_Image
from APL import Addedpathlength
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
        self.APL, self.APL_length_ratio, self.APL_volume_ratio = self.getAPL() # Dictionaries
        self.allmetrics = ["DICE", "Hausdorff", "MSD"] #og add APL når den er klar. 

    def __str__(self):
        MetricPrint =   f'PatientID: {self.PatientID}\n' + \
                        f'OAR: {self.OAR}\n' + \
                        f'DICE: {self.DICE}\n' + \
                        f'Hausdorff: {self.Hausdorff}\n' + \
                        f'Mean Surface Distance: {self.MSD}\n' + \
                        f'Added path length: {self.APL}\n' + \
                        f'APL length ratio: {self.APL_length_ratio}\n' + \
                        f'APL volume ratio: {self.APL_volume_ratio}'
        
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
            dicecomputer.Execute(P2>0.5,P1>0.5) #Use P1, P2 > 0.5 so we don't compare overlap of entries  == 0. 
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
        APL_dict = {}
        APL_length_ratio_dict = {}
        APL_volume_ratio_dict = {}
        for i, comp in enumerate(self.comparisons):
            APL_dict[comp] = "None" + str(i)
            APL_length_ratio_dict[comp] = "None" + str(i)
            APL_volume_ratio_dict[comp] = "None" + str(i)
        
        for met1, met2 in self.comparisons:
            P1 = getattr(self, met1)
            P2 = getattr(self, met2)
            #Import py-script to get APL
            values = Addedpathlength(P1,P2)
            APL_dict[(met1,met2)] = values.APL
            APL_length_ratio_dict[(met1, met2)] = values.APL_line_ratio
            APL_volume_ratio_dict[(met1, met2)] = values.APL_volume_ratio
        
        return APL_dict, APL_length_ratio_dict, APL_volume_ratio_dict

    def getAll(self):
        getAll_dict = {}
        for i, metr in enumerate(self.allmetrics):
            getAll_dict[metr] = "None" + str(i)
        
        for metr in self.allmetrics:
            res = getattr(self, metr)
            getAll_dict[metr] = res

        return getAll_dict




#Test
PatientID = "1cbDrFdyzAXjFICMJ58Hmja9U"
Segment = "mandible" 
Methods = ["GT", "DL", "DLB"]
print(Path(PatientID, Methods[0]).File)

MET = Metrics(PatientID, Segment, Methods)
print(MET)


