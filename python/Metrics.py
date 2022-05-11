"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      Metrics.py

Discribtion:    Skabelon for nye filer.
"""

# Initialization
print(f"Running {__name__}")


# Imports
import SimpleITK as ITK


# Import other files
from DataReader import Path
from DataPreparation import OAR_Image
from EditedPathLength import EPL_Metric


# Classes and functions
class Metrics_Info():

    def __init__(self, ImageA : OAR_Image = OAR_Image(),
                 ImageB : OAR_Image = OAR_Image(), Tolerence : int = 0):

        self.ImageA = ImageA
        self.ImageB = ImageB
        self.Tolerance = Tolerence
        self.Comparison = self.getComparison()
        self.Empty = self.ImageA.Exists and self.ImageB.Exists

        if self.Empty:
            self.DICE = self.getDICE()
            self.Hausdorff = self.getHausdorff()
            self.MSD = self.getMSD()
            self.EPL, self.LineRatio, self.VolumeRatio = self.getEPL()

        else:
            self.DICE = None
            self.Hausdorff = None
            self.MSD = None
            self.EPL = None
            self.LineRatio = None
            self.VolumeRatio = None
        

    def __str__(self):
        msg = (
            f'PatientID: {self.ImageA.Path.ID}\n'
            f'OAR: {self.ImageA.OAR}\n'
            f'Comparison: {self.Comparison}\n'
            f'DICE: {self.DICE}\n'
            f'Hausdorff: {self.Hausdorff}\n'
            f'Mean Surface Distance: {self.MSD}\n'
            f'Edited Path Length: {self.EPL}\n'
            f'Line Ratio: {self.LineRatio}\n'
            f'Volume Ratio: {self.VolumeRatio}'
        )
        
        return msg


    def getComparison(self):
        M1 = self.ImageA.Path.Method
        M2 = self.ImageB.Path.Method

        return f'{M1} vs {M2}'

    
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


    def getEPL(self):
        EPL = EPL_Metric(self.ImageA, self.ImageB, self.Tolerance)

        return EPL.EPL, EPL.LineRatio, EPL.VolumeRatio


    def getAttributes(self):
        
        output = {'ID' : [self.ImageA.Path.ID],
                  'Date' : [self.ImageA.Path.Date],
                  'DICE': [self.DICE],
                  'Hausdorff' : [self.Hausdorff],
                  'MSD' : [self.MSD],
                  'EPL' : [self.EPL],
                  'LineRatio' : [self.LineRatio],
                  'VolumeRatio' : [self.VolumeRatio]}
        return output

# Class tester
if __name__ == '__main__':
    ID = '4Prj3A5sMvSv1sK4u5ihkzlnU'
    Date = '20190129'
    P1 = Path(ID, Date, 'GT')
    P2 = Path(ID, Date, 'ATLAS')

    IA = OAR_Image(P1, 'brain')
    IB = OAR_Image(P2, 'brain')

    print(IA)
    print(IB)

    MI = Metrics_Info(IA, IB)
    print(MI)

    print('\nEmpty:')
    MI2 = Metrics_Info()
    print(MI2)
