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
from functools import lru_cache

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
        self.TotalAreaAB = 0

        self.SliceValuesEPL = []
        self.SliceLineSegmentsV = []
        self.SliceLineSegmentsH = []
        self.SlicePointsA = []
        self.SlicePointsB = []

        self.EPL = self.getEPL()
        self.LineEPL = self.getLineEPL()
        self.VolumeEPL = self.getVolumeEPL(self.TotalAreaA)
        self.VolumeEPL2 = self.getVolumeEPL(self.TotalAreaAB)


    def __str__(self):
        msg = (
            f'EPL: {self.EPL}\n'
            f'EPL (Line Ratio): {self.LineEPL}\n'
            f'EPL (Volume Ratio): {self.VolumeEPL}'
        )

        return msg


    def getLine(self, p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        if x0 == x1:
            x = x0
            y = (y0 + y1)/2
            
            return ((x - 0.5, y), (x + 0.5, y))

        else:
            y = y0
            x = (x0 + x1)/2
            
            return ((x, y - 0.5), (x, y + 0.5))

    
    def findPoints(self, A):
        return {(x, y) for y, x in zip(*np.nonzero(A))}


    def findEdgePoints(self, points, tol = 0):
    
        @lru_cache
        def isEdge(x, y, tol = 0):
            """
            Returns 'True' if the point (x, y) can get to the background/edge in
            'tol' steps.
            """
            nonlocal points

            if tol == 0:
                return (x, y) not in points # not in points = point is edge
            
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if isEdge(x + dx, y + dy, tol - 1):
                    return True 
            
            return False # return false if could not get to the edge.

        if tol:
            return {(x, y) for x, y in points if isEdge(x, y, tol)}
        else:
            return set()


    def findLines(self, points, tol = 0):
        edgePoints = self.findEdgePoints(points, tol)

        @lru_cache
        def findLinesRecursive(x, y, tol = 0):
            nonlocal points
            nonlocal edgePoints

            lines = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if tol == 0:
                    if (((x, y) in edgePoints) or 
                        ((x + dx, y + dy) in edgePoints) or
                        ((x + dx, y + dy) not in points)   
                    ):
                        lines += [self.getLine((x, y), (x + dx, y + dy))]
                else:
                    lines += [*findLinesRecursive(x + dx, y + dy, tol - 1)]
            
            return lines

        allLines = set()
        for p in points:
            allLines |= set(findLinesRecursive(*p, tol))

        vlines = set()
        hlines = set()
        for (x0, y0), (x1, y1) in allLines:
            if x0 == x1:
                vlines.add(((x0, y0), (x1, y1)))
            else:
                hlines.add(((x0, y0), (x1, y1)))

        return vlines, hlines


    def getEPL(self):
        for z in range(self.Slices):
            pointsA = self.findPoints(self.A[z])
            self.SlicePointsA.append(pointsA)

            pointsB = self.findPoints(self.B[z])
            self.SlicePointsB.append(pointsB)

            vLinesA, hLinesA = self.findLines(pointsA)
            vLinesB, hLinesB = self.findLines(pointsB, self.Tolerance)

            vDiff = vLinesA - vLinesB
            self.SliceLineSegmentsV.append(vDiff)
            
            hDiff = hLinesA - hLinesB
            self.SliceLineSegmentsH.append(hDiff)

            self.TotalLengthA += (len(vLinesA)* self.Height) + (len(hLinesA) * self.Width)
            self.TotalAreaA += (self.Width + self.Height) * len(pointsA)
            self.TotalAreaAB += (self.Width + self.Height) * len(pointsA & pointsB)
            EPL = len(vDiff) * self.Height + len(hDiff) * self.Width
            self.SliceValuesEPL.append(EPL)

        return sum(self.SliceValuesEPL)


    def getLineEPL(self):
        try:
            return self.EPL / self.TotalLengthA
        except ZeroDivisionError:
            return 0
        

    def getVolumeEPL(self, area):
        try: 
            return self.EPL / area
        except ZeroDivisionError:
            return 0


# Functions only used for testing
if __name__ == '__main__':
    from time import process_time as pt
    import matplotlib.ticker as plticker
    import matplotlib.pyplot as plt

    def readExample(file):
        array = []
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                values = [int(c) for c in line.split()]
                array.append(values)
        
        return np.array(array)


    def getLine(p0, p1):
        x0, y0 = p0
        x1, y1 = p1

        if x0 == x1:
            x = x0
            y = (y0 + y1)/2
            return ((x - 0.5, y), (x + 0.5, y))
        else:
            y = y0
            x = (x0 + x1)/2
            return ((x, y - 0.5), (x, y + 0.5))

    
    def findPoints(A, tol = 0):
    
        @lru_cache
        def isEdge(x, y, tol = 0):
            nonlocal A

            if tol == 0:
                return not A[y, x]
            
            if A[y, x]: # != 0:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if isEdge(x + dx, y + dy, tol - 1):
                        return True
            
                return False
            
            else:
                return True


        points = [(x, y) for y, x in zip(*np.nonzero(A))]
        edges = [(x, y) for x, y in points if isEdge(x, y, tol)] if tol else []

        return points, edges


    def findLines(A, tol = 0):
        points, edgePoints = findPoints(A, tol)

        @lru_cache
        def findLinesRecursive(x, y, tol = 0):
            nonlocal A
            nonlocal edgePoints

            lines = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if tol == 0:
                    if (((x, y) in edgePoints) or 
                        ((x + dx, y + dy) in edgePoints) or
                        (not (A[y + dy, x + dx]))   
                    ):
                        lines += [getLine((x, y), (x + dx, y + dy))]
                else:
                    lines += [*findLinesRecursive(x + dx, y + dy, tol - 1)]
            
            return lines

        allLines = set()
        for p in points:
            allLines |= set(findLinesRecursive(*p, tol))

        vlines = set()
        hlines = set()
        for (x0, y0), (x1, y1) in allLines:
            if x0 == x1:
                vlines.add(((x0, y0), (x1, y1)))
            else:
                hlines.add(((x0, y0), (x1, y1)))

        return vlines, hlines


    def plotPoints(points, col = 'b', mark = 'o'):
        x, y = zip(*points)
        y = [-y_ for y_ in y]
        plt.plot(x, y, color = col, marker = mark, ls = '')


    def plotLines(lines):
        for (x0, y0), (x1, y1) in lines:
            if x0 == x1:
                plt.vlines(x0, ymin = -y0, ymax = -y1, colors = 'b', ls = 'dashdot')
            else:
                plt.hlines(-y0, xmin = x0, xmax = x1, colors = 'b', ls = 'dashdot')


    def plot(xlen, ylen, title = ''):
        plt.xlim([0, xlen])
        plt.ylim([-ylen, 0])
        plt.grid(linestyle='-', linewidth=0.25, which = 'both')

        ax = plt.gca()
        loc = plticker.MultipleLocator(base=1)
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)
        ax.set_xticks(np.arange(0, xlen))
        ax.set_yticks(np.arange(ylen, 0))
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.set_aspect(1)

        plt.title(title)
        plt.show()


# Actual testing
if __name__ == '__main__':
    P1 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'GT')
    P2 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'DL')

    for Segment in ['brain', 'brainstem', 'parotid_merged', 'pcm_low', \
    'pcm_mid', 'pcm_low', 'spinalcord', 'thyroid']:
        IMGA = OAR_Image(P1, Segment)
        IMGB = OAR_Image(P2, Segment)

        for testTol in [0, 1, 2, 3]:
            t0 = pt()
            M = EPL_Metric(IMGA, IMGB, testTol)
            t1 = pt()
            print()
            print(f'TestTime: {t1-t0}, Segment: {Segment}, Tolerance: {testTol}')
            print(M)
    
