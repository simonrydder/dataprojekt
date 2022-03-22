"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Metrics.py

Discribtion:    Skabelon for nye filer.
"""

# Imports
import SimpleITK as ITK

# Import other files
from DataReader import Path
from DataPreparation import OAR_Image
from APL import AddedPathLength
# from DICE import DICE

# Classes and functions
class Metrics():

    def __init__(self, ID, segment, methodA, methodB):
        self.PatientID = ID     # As id-type
        self.OAR = segment      # As string i.e. "Brainstem"
        self.MethodA = methodA.upper()  # "GT", "DL", "DLB", "ATLAS" - Typically "GT"
        self.MethodB = methodB.upper()  # "GT", "DL", "DLB", "ALTAS" - Typically not "GT"
        self.Comparison = f'{self.MethodA} vs {self.MethodB}'
        self.ImageA = self.getImage(self.MethodA)    # OAR_Image from method A
        self.ImageB = self.getImage(self.MethodB)    # OAR_Image from method B
        self.DICE = self.getDICE()
        self.Hausdorff = self.getHausdorff()
        self.MSD = self.getMSD()
        self.APL, self.APL_length_ratio, self.APL_volume_ratio = self.getAPL()

    def __str__(self):
        MetricPrint =   f'PatientID: {self.PatientID}\n' + \
                        f'OAR: {self.OAR}\n' + \
                        f'Comparison: {self.Comparison}\n' + \
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
        A = self.ImageA.Image   # ITK image
        B = self.ImageB.Image   # ITK image

        dicecomputer = ITK.LabelOverlapMeasuresImageFilter()
        dicecomputer.Execute(A > 0.5, B > 0.5)

        return dicecomputer.GetDiceCoefficient()

    def getHausdorff(self):
        A = self.ImageA.Image   # ITK image
        B = self.ImageB.Image   # ITK image

        hauscomputer = ITK.HausdorffDistanceImageFilter()
        hauscomputer.Execute(A > 0.5, B > 0.5)

        return hauscomputer.GetHausdorffDistance()

    def getMSD(self):
        A = self.ImageA.Image   # ITK image
        B = self.ImageB.Image   # ITK image

        hauscomputer = ITK.HausdorffDistanceImageFilter()
        hauscomputer.Execute(A > 0.5, B > 0.5)

        return hauscomputer.GetAverageHausdorffDistance()

    def getAPL(self):
        APL_Objekt = AddedPathLength(self.ImageA, self.ImageB)

        return APL_Objekt.APL, APL_Objekt.APL_line_ratio, APL_Objekt.APL_volume_ratio

# Test
PatientID = "1cbDrFdyzAXjFICMJ58Hmja9U"
Segment = "BrainStem"
Methods = ["GT", "DL"]

print(Path(PatientID, Methods[0]).File)

MET = Metrics(PatientID, Segment, Methods[0], Methods[1])
print(MET)
