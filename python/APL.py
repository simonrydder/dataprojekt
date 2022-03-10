"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        10/03/2022

File name:      APL.py

Discription:    Class to compute added path length between two images
                Inputs: img1: the "true" image img2: the "false" image
                outputs: 3 callable attributes 
                APL: Added path length in mm
                APL_line_ratio: ratio between Added path length and the path length of the "true" image
                APL_volume_ratio: ratio between Added path length and the volume of the "true" image.
"""
#Imports
import numpy as np

#Import other files
import DataPreparation


#Classes and functions
class Addedpathlength():
    def __init__(self,img1,img2):
        self.width,self.height, _ = OAR_DL.Spacing
        _,_, self.z = img1.Shape
        self.A = img1.GetArray()
        self.B = img2.GetArray()
        self.APL = self.getAPL()
        self.APL_line_ratio = self.getLineRatio()
        self.APL_volume_ratio = self.getAPLvolume()

    def getAPL(self):
        APL_total = 0
        self.True_Length = 0
        self.True_Area = 0
        for i in range(self.z):
            coordsA = self.findCoordinates(self.A[i])
            coordsB = self.findCoordinates(self.B[i])
            VA, HA = self.findLines(coordsA)
            VB, HB = self.findLines(coordsB)

            VA = set(VA)
            HA = set(HA)
            VB = set(VB)
            HB = set(HB)
            vrest = VA - VB
            hrest = HA - HB

            # vrest = (set(VA) - set(VB))
            # hrest = (set(HA) - set(HB))

            self.True_Length += len(VA)*self.height+len(HA)*self.width
            self.True_Area += len(coordsA)*self.height+len(coordsA)*self.width

            APL_total += len(vrest) * self.height + len(hrest) * self.width

        return APL_total

    def getLineRatio(self):
        return self.APL/self.True_Length

    def getAPLvolume(self):
        return self.APL/self.True_Area

    def findCoordinates(self,array):
        """
        Input:  An array A[y][x]
        Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] == 1.
        """
        N = len(array)
        coords = np.where(array > 0)
        return [(x + 1, N - y) for y, x in zip(*coords)]

    def findLines(self,coordinates):
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


# Test

fileDL = "A:\\Task5041_OARBoundsMergedDSCTOnly\\fold_0\\4Prj3A5sMvSv1sK4u5ihkzlnU&20190129.nii.gz"
fileGT = "A:\\Task5041_OARBoundsMergedDSCTOnly\\cts\labels\\4Prj3A5sMvSv1sK4u5ihkzlnU&20190129.nii.gz"

segment = 'brainstem'

OAR_DL = DataPreparation.OAR_Image(fileDL,segment)
OAR_GT = DataPreparation.OAR_Image(fileGT,segment)


test = Addedpathlength(OAR_GT,OAR_DL)

test.APL
test.APL_line_ratio
test.APL_volume_ratio