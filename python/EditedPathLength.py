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
from DataPreparation import OAR_Image
from DataReader import Path


#Classes and functions
class EPL_Metric():
    def __init__(self, model : OAR_Image = OAR_Image(),
                 gt : OAR_Image = OAR_Image(), Tolerance : int = 0):

        # Inputs
        self.model = model.GetArray()  # np.array (z, y, x)
        self.gt = gt.GetArray()  # np.array (z, y, x)
        self.Tolerance = Tolerance


        # Spacing and shape
        self.Width, self.Height, _ = model.Spacing   # x, y, z
        _, _, self.Slices = gt.Shape   # x, y, z
        

        # Ekstra list to save slice information to dashboard
        self.SliceEPL = []
        self.SliceLR = []           # LR = Line Ratio
        self.SliceVR = []           # VR = Volume Ratio
        self.SliceLinesModel = []   
        self.SliceLinesChanged = [] 
        self.SlicePointsModel = []  # Points for model pr. slice
        self.SlicePointsGT = []     # Points for 'ground truth' pr. slice


        # Metrics
        self.EPL = 0                # Defined as the total length of the edited path.
        self.TotalLength = 0        # Defined as the total lenght after change.
        self.LineRatio = 0          # Defined as the ratio between EPL and TotalLength

        self.TotalAreaChanged = 0   # Defined as the total area changed.
        self.TotalArea = 0          # Defined as the total area after change.
        self.VolumeRatio = 0        # Defined as the ratio between TotalAreaChanged and TotalArea

        self.updateMetrics()


    def __str__(self):
        msg = (
            f'EPL: {self.EPL}\n'
            f'EPL (Line Ratio): {self.LineEPL}\n'
            f'EPL (Volume Ratio): {self.VolumeEPL}'
        )

        return msg

    
    def findPoints(self, array):
        """ 
        Function take a 2D array where the rows of the array correspond to the 
        y-axis and the columns correspond to the x-axis and returns a set of 
        (x, y)-coordinates where the input array are non-zero.        
        """
        return {(x, y) for y, x in zip(*np.nonzero(array))}


    def findResultingPoints(self, gtPoints, modelPoints):
        """
        Function take two set of points, where modelPoints are non-zero points 
        of a model that a doctor gets and edit and gtPoints are non-zero points
        of the 'ground truth'. A tolerance of 0 mean the modelPoints are 
        changed exactly to the 'ground truth' where any positive number indicates
        the number of pixels (not diagonally) the model are allowed to be away
        from the 'ground truth'.
        The function returns the resulting points which are a union of modelPoints
        that are at most tolerance pixels away from the 'grund truht' and gtPoints 
        that are not on the edge of the segmentation.
        """        
        
        def findValidModelPoints(tol = 0):
            """
            Function that finds the modelPoints which are at most tol pixels 
            away from the gtPoints.
            """
            nonlocal gtPoints, modelPoints

            @lru_cache
            def isValid(x, y, tol = 0):
                
                if tol == 0:
                    return (x, y) in gtPoints
                
                for dx, dy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if isValid(x + dx, y + dy, tol - 1):
                        return True
                
                return False

            return {(x, y) for x, y in modelPoints if isValid(x, y, tol)}


        def findValidGTPoints(tol = 0):
            """
            Function that finds the center gtPoints and removes the edge points.
            Where an edge point is defined as a point which can reach the background
            in tol (not diagonally) pixels.
            """
            nonlocal gtPoints

            @lru_cache
            def isEdge(x, y, tol = 0):

                if tol == 0:
                    return (x, y) not in gtPoints

                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    if isEdge(x + dx, y + dy, tol - 1):
                        return True 
            
                return False # return false if could not get to the edge.

            return {(x, y) for x, y in gtPoints if not isEdge(x, y, tol)}

        ValidModelPoints = findValidModelPoints(self.Tolerance) 
        ValidGTPoints = findValidGTPoints(self.Tolerance)

        return ValidModelPoints | ValidGTPoints


    def findLines(self, coordinates):
        """
        Input:  A list of coordinates for the center of a pixel.
        Outout: Two lists of linesegments. One for horizontal linesegments and 
                one for vertical linesegments.
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


    def updateMetrics(self):
        
        for z in range(self.Slices):
            pM = self.findPoints(self.model[z])
            pGT = self.findPoints(self.gt[z])
            pRes = self.findResultingPoints(pGT, pM)
            
            vM, hM = self.findLines(pM)
            vRes, hRes = self.findLines(pRes)
            vEPL, hEPL = vRes - vM, hRes - hM

            SliceEPL = len(vRes - vM)*self.Height + len(hRes - hM)*self.Width
            self.EPL += SliceEPL

            SliceLine = len(vRes) * self.Height + len(hRes) * self.Width
            self.TotalLength += SliceLine

            SliceArea = self.Height*self.Width * len(pRes)
            self.TotalArea += SliceArea

            SliceAreaChanged = self.Height*self.Width * len(pM ^ pRes)
            self.TotalAreaChanged += SliceAreaChanged

            # Add slice results to lists for plotting i dashboard.
            self.SlicePointsModel.append(pM)
            self.SlicePointsGT.append(pGT)
            self.SliceLinesModel.append(vM | hM)
            self.SliceLinesChanged.append(vEPL | hEPL)
            self.SliceEPL.append(SliceEPL)
            SliceLR = SliceEPL / SliceLine if SliceLine != 0 else 0
            self.SliceLR.append(SliceLR)
            SliceVR = SliceAreaChanged / SliceArea if SliceArea != 0 else 0
            self.SliceVR.append(SliceVR)

        self.LineRatio = self.updateLineRatio()
        self.VolumeRatio = self.updateVolumeRatio()


    def updateLineRatio(self):
        try:
            return self.EPL / self.TotalLength
        except ZeroDivisionError:
            return 0
        

    def updateVolumeRatio(self):
        try: 
            return self.TotalAreaChanged / self.TotalArea
        except ZeroDivisionError:
            return 0



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


    def plotPoints(points, col = 'k', mark = '.'):
            x, y = zip(*points)
            plt.plot(x, y, color = col, marker = mark, ls = '')


    def plotLines(lines, color = 'b', style = 'dashdot', width = 1):
        for (x0, y0), (x1, y1) in lines:
            if x0 == x1:
                plt.vlines(x0, ymin = y0, ymax = y1, colors = color, ls = style, lw = width)
            else:
                plt.hlines(y0, xmin = x0, xmax = x1, colors = color, ls = style, lw = width)


    def plot(xlim, ylim, title = ''):
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.grid(linestyle='-', linewidth=0.25, which = 'both')

        ax = plt.gca()
        loc = plticker.MultipleLocator(base=1)
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)
        ax.set_xticks(np.arange(*xlim))
        ax.set_yticks(np.arange(*ylim))
        ax.xaxis.set_ticklabels([])
        ax.yaxis.set_ticklabels([])
        ax.set_aspect(1)

        plt.title(title)
        plt.show()


if __name__ == '__main__':
    P1 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'GT')
    P2 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'DL')

    Segment = 'brainstem'
    IMGA = OAR_Image(P1, Segment)
    IMGB = OAR_Image(P2, Segment)

    EPL = EPL_Metric(model = IMGB, gt = IMGA, Tolerance = 1)

    print(f'{EPL.EPL = } and {EPL.TotalLength = }: {EPL.LineRatio = }')
    print(f'{EPL.TotalAreaChanged = } and {EPL.TotalArea = }: {EPL.VolumeRatio = }')

    nPointsGT = [len(points) for points in EPL.SlicePointsGT]
    nPointsM = [len(points) for points in EPL.SlicePointsModel]
    nPoints = [gt + m for gt, m in zip(nPointsGT, nPointsM)]
    layer = np.argmax(nPoints)

    xGT, yGT = zip(*EPL.SlicePointsGT[layer])
    xM, yM = zip(*EPL.SlicePointsModel[layer])

    buffer = 3
    xlimits = [min(xGT + xM) - buffer, max(xGT + xM) + buffer + 1]
    ylimits = [min(yGT + yM) - buffer, max(yGT + yM) + buffer + 1]

    plotLines(EPL.SliceLinesModel[layer])
    plotLines(EPL.SliceLinesChanged[layer], color = 'r', style = 'dashed')
    plotPoints(EPL.SlicePointsGT[layer])
    plot(xlimits, ylimits,
        title = f'{Segment}[{layer}]: EPL = {EPL.SliceEPL[layer]}, LineRatio = {EPL.SliceLR[layer]}, VolumeRatio = {EPL.SliceVR[layer]}')

    print('Done')


# Creating new examples
if False:
    P1 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'GT')
    P2 = Path('4Prj3A5sMvSv1sK4u5ihkzlnU', '20190129', 'DL')

    Segment = 'parotid_merged'
    IMGA = OAR_Image(P1, Segment)
    IMGB = OAR_Image(P2, Segment)

    A = IMGA.GetArray()
    B = IMGB.GetArray()
    Slice = np.argmax(np.sum(np.sum(A, axis = 1), axis = 1) + np.sum(np.sum(B, axis = 1), axis = 1))
    A = A[Slice]
    B = B[Slice]
    xA, yA = A.nonzero()
    xB, yB = B.nonzero()
    x_min = min(list(xA) + list(xB)) - 3
    x_max = max(list(xA) + list(xB)) + 3
    y_min = min(list(yA) + list(yB)) - 3
    y_max = max(list(yA) + list(yB)) + 3

    A = A[x_min:x_max, y_min:y_max]
    B = B[x_min:x_max, y_min:y_max]

    with open(f'EPL_examples\\{Segment}A{Slice}.txt', 'w') as f:
        for row in A[::-1]:
            f.write(' '.join([str(n) for n in list(row)]) + '\n')

    with open(f'EPL_examples\\{Segment}B{Slice}.txt', 'w') as f:
        for row in B[::-1]:
            f.write(' '.join([str(n) for n in list(row)]) + '\n')

