"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      skabelon.py

Discribtion:    Skabelon for nye filer.
"""

# Imports
# from matplotlib import cm
import numpy as np
# import SimpleITK as ITK
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
# from pyparsing import line_start

# Import other files
# from Metrics import Metrics
from DataPreparation import OAR_Image
from DataReader import Path

# Classes and functions

def readExample(file):
    """
    Input:  File name of type "AddedPathLengthExamples\example#.txt". Border of '0's is needed.
    Output: Two numpy arrays. The first being the Truth and the second being the Other
    """

    def constructArray(lines):
        """
        Input:  A list of strings.
        Output: A numpy array.
        """
        array = []
        for line in lines:
            values = [int(c) for c in line.split()]
            array.append(values)

        return np.array(array)

    with open(file) as f:
        lines = f.readlines()

    n = len(lines)//2

    A = constructArray(lines[:n])   # Truth
    B = constructArray(lines[n+1:]) # Other

    return A, B


def findCoordinates(array):
    """
    Input:  An array A[y][x]
    Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] == 1.
    """
    N = len(A)
    coords = np.where(array > 0)
    return [(x + 1, N - y) for y, x in zip(*coords)]


def getEdges(coordinates):
    """
    Input:  An array A[y][x].
    Output: A list of coordinates of the form (x + 1, len(A) - y), where A[y][x] is an edge.
    """

    # out = []
    # for x, y in coordinates:
    #     neighbours = [(x_, y_) for x_ in range(x-1, x+2) for y_ in range(y-1, y+2)]
    #     if len(set(coordinates) & set(neighbours)) < 9: # Finding the intersection of points.
    #         out.append((x, y))

    # return out

    return [(x, y) for x, y in coordinates
            if len(set(coordinates) & {(a, b) for a in range(x-1, x+2) for b in range(y-1, y+2)}) < 9]


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


def plot(A, B, example = ""):
    """
    Input:  Two arrays A[y][x] and B[y][x].
    Output: A figure plot.
    """

    # Check shape of inputs.
    assert A.shape == B.shape, "A and B is not of same size"

    # Defining the number of pixels in the y-dimension (n) and the x-dimension (m)
    n, m = A.shape
    print(n, m)

    coordsA = findCoordinates(A)
    x, y = zip(*coordsA)
    plt.plot(x, y, 'bo')

    edgesA = getEdges(coordsA)
    x, y = list(zip(*edgesA))
    plt.plot(x, y, 'r*')

    VA, HA = findLines(coordsA)

    for line in VA:
        (x, y0), (_, y1) = line
        plt.vlines(x, ymin = y0, ymax = y1, colors = 'r', linestyles = 'dashdot')

    for line in HA:
        (x0, y), (x1, _) = line
        plt.hlines(y, xmin = x0, xmax = x1, colors = 'r', linestyles = 'dashdot')

    
    coordsB = findCoordinates(B)
    x, y = zip(*coordsB)
    plt.plot(x, y, 'go')

    edgesB = getEdges(coordsB)
    x, y = list(zip(*edgesB))
    plt.plot(x, y, 'y*')

    VB, HB = findLines(coordsB)

    for line in VB:
        (x, y0), (_, y1) = line
        plt.vlines(x, ymin = y0, ymax = y1, colors = 'g', linestyles = 'dashed')

    for line in HB:
        (x0, y), (x1, _) = line
        plt.hlines(y, xmin = x0, xmax = x1, colors = 'g', linestyles = 'dashed')

    Vrest = set(VA) - set(VB)
    Hrest = set(HA) - set(HB)
    example = str(len(Vrest) + len(Hrest))


    plt.grid(linestyle='-', linewidth=0.25, which = 'both')
    plt.xlim([1, m])
    plt.ylim([1, n])

    # Set grid line spacing to 1.
    ax = plt.gca()
    loc = plticker.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    ax.set_aspect(1)

    # Title
    plt.title("Added Path length Example" + example)

    # Plot figure
    plt.show()


# Run file (optional)
example = 3
A, B = readExample("AddedPathLengthExamples\\example%d.txt" %example)

plot(A, B, str(example))

# Test on real image
pathA = Path("0ku1qeiExUvrl65s5bvTX5fKA", "GT")
pathB = Path("0ku1qeiExUvrl65s5bvTX5fKA", "DL")

OAR_A = OAR_Image(pathA.File, "brainstem")
OAR_B = OAR_Image(pathB.File, "brainstem")

print(OAR_A.Shape, OAR_B.Shape)

i = OAR_A.Shape[2]//2 # Shape[2] = z
A = OAR_A.GetArray()[i]
B = OAR_B.GetArray()[i]

plot(A, B)

# Other
