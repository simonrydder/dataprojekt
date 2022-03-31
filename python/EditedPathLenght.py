"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        10/03/2022

File name:      EditedPathLength.py

Discription:    Implements the class EPL_Metric. The class takes two inputs:
                - ImageA <class 'OAR_Image'>
                - ImageB <class 'OAR_Image'>
                and calculate three metrics:
                - EPL: The total lenght [mm] going from ImageB to ImageA
                - LineEPL: A ratio defined as EPL devided with the total length
                           of ImageA. Class to compute three different metricsadded path length between two images
                Inputs: img1: the "true" image img2: the "false" image
                outputs: 3 callable attributes 
                APL: Added path length in mm
                APL_line_ratio: ratio between Added path length and the path length of the "true" image
                APL_volume_ratio: ratio between Added path length and the volume of the "true" image.
"""

# Initialization
print(f"Running {__name__}")


#Imports
import numpy as np


#Import other files
from DataPreparation2 import OAR_Image
from DataReader2 import Path


#Classes and functions
class EPL_Metric():
    def __init__(self, ImageA : OAR_Image = OAR_Image(),
                 ImageB : OAR_Image = OAR_Image(), Tolerance : int = 0):
        self.A = ImageA.GetArray()  # np.array (z, y, x)
        self.B = ImageB.GetArray()  # np.array (z, y, x)
        self.Tolerance = Tolerance

        self.Width, self.Height, _ = ImageA.Spacing   # x, y, z
        _, _, self.Slices = ImageA.Shape   # x, y, z
        
        self.TotalLengthA = 0
        self.TotalAreaA = 0
        self.EPL = self.getEPL()
        self.LineEPL = self.getLineEPL()
        self.VolumeEPL = self.getVolumeEPL()

    def __str__(self):
        msg = (
            f'EPL: {self.EPL}\n'
            f'EPL (Line Ratio): {self.LineEPL}\n'
            f'EPL (Volume Ratio): {self.VolumeEPL}'
        )

        return msg

    def getEPL(self):
        ELP = 0
        for z in range(self.Slices):
            coordsA = self.findCoordinates(self.A[z])   # Coordinates for Image A
            coordsB = self.findCoordinates(self.B[z])   # Coordinates for Image B
            VA, HA = self.findLines(coordsA)    # Sets of Vertical and Horizontal Lines for A
            VB, HB = self.findLines(coordsB)    # Sets of Vertical and Horizontal Lines for B



            vrest = VA - VB
            hrest = HA - HB

            self.TotalLengthA += (len(VA) * self.Height) + (len(HA) * self.Width)
            self.TotalAreaA += (self.Height + self.Width) * len(coordsA)     # For area of A
            # self.TotalAreaA += (self.height + self.width) * len(coordsA & coordsB)     # For area of the intersection of A and B

            ELP += len(vrest) * self.Height + len(hrest) * self.Width

        return ELP

    def getLineEPL(self):
        try:
            return self.EPL / self.TotalLengthA
        except ZeroDivisionError:
            return 0
        

    def getVolumeEPL(self):
        try: 
            return self.EPL / self.TotalAreaA
        except ZeroDivisionError:
            return 0

    def findCoordinates(self, array):
        """
        Input:  An array A[y][x]
        Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] > 0.
        """

        N = len(array)
        coords = np.where(array > 0)
        points = {(x + 1, N - y) for y, x in zip(*coords)}

        return points

    def findLines(self, coordinates):
        """
        Input:  A list of coordinates for the center of a pixel.
        Outout: Two lists of linesegments. One for horizontal linesegments and one for vertical linesegments.
        """

        verticals = {}
        horizontals = {}

        for x, y in coordinates:
            left  = ((x - 0.5, y - 0.5), (x - 0.5, y + 0.5)) # left edge line
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
        Vlines = {key for key, value in verticals.items() if value == 1}
        Hlines = {key for key, value in horizontals.items() if value == 1}
        
        return Vlines, Hlines


# Test
if __name__ == '__main__2':
    points = {(1,1),(1,2)}
    p_tol = {(0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (2,1), (2,2)}

    def addTolerance(x, y, tol):
        if tol == 0:
            return [(x, y)]        

        new_points = [(x, y)]

        down = (x, y - 1)
        up = (x, y + 1)
        left = (x - 1, y)
        right = (x + 1, y)
        for direction in down, up, left, right:
            new_points += addTolerance(*direction, tol - 1)
        
        return new_points

    p_test = {(x, y) for point in points for (x, y) in addTolerance(*point, tol = 1)}
    print('Test addTolerance():')
    if p_tol == p_test:
        print(f'Test succeeded\n')
    else:
        print(f'Test failed\nGot {p_test}\nExpected {p_tol}')

    from time import time

    ID = '4Prj3A5sMvSv1sK4u5ihkzlnU'
    Date = '20190129'
    P1 = Path(ID, Date, 'GT')
    P2 = Path(ID, Date, 'DL')

    for segment in ['brainstem', 'pcm_low', 'parotid_merged']:
        OARA = OAR_Image(P1, segment)
        print(OARA)
        OARB = OAR_Image(P2, segment)

        for tol in [0]:
            print(f'Test time of {segment} with {tol = }:')
            t0 = time()
            res = EPL_Metric(OARA, OARB, tol)
            t1 = time()
            print(res)
            print(f'In {t1-t0} sec\n')
    
    empty = EPL_Metric()
    print(empty)

if __name__ == '__main__':
    from time import process_time as pt
    P1 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'GT')
    P2 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'DL')

    for Segment in ['brain', 'brainstem', 'parotid_merged', 'pcm_low', \
        'pcm_mid', 'pcm_low', 'spinalcord', 'thyroid']:
        IMGA = OAR_Image(P1, Segment)
        IMGB = OAR_Image(P2, Segment)

        t0 = pt()
        M = EPL_Metric(IMGA, IMGB, 0)
        t1 = pt()
        print()
        print(f'TestTime: {t1-t0}, Segment: {Segment}, Tolerance: 0')
        print(M)