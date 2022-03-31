"""
Authors:        Alex Kolby, Eskild Hjerrild Andersen, Simon Rydder

Created:        21/02/2022

File name:      ValidateMatrices.py

Discribtion:    This file is a visual check of the implemented 
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

# Import other files
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
    N = len(array)
    coords = np.where(array > 0)
    return [(x + 1, N - y) for y, x in zip(*coords)]


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


def findLimits(x, y, limits = []):
    Xmin = min(x) - 1
    Xmax = max(x) + 1
    Ymin = min(y) - 1
    Ymax = max(y) + 1
    
    if limits != []:
        Xmin = min(Xmin, limits[0][0])
        Xmax = max(Xmax, limits[0][1])
        Ymin = min(Ymin, limits[1][0])
        Ymax = max(Ymax, limits[1][1])

    return [(Xmin, Xmax), (Ymin, Ymax)]

def plot(A, B, suptitle = ""):
    """
    Input:  Two arrays A[y][x] and B[y][x].
    Output: A figure plot.
    """

    # Check shape of inputs.
    assert A.shape == B.shape, "A and B is not of same size"

    # Defining the number of pixels in the y-dimension (n) and the x-dimension (m)
    n, m = A.shape

    # Plotting A
    coordsA = findCoordinates(A)
    x, y = zip(*coordsA)
    limits = findLimits(x, y)
    plt.plot(x, y, color = 'b', marker = 'o', ls = '', label = "A (Truth): Pixels")

    VA, HA = findLines(coordsA)

    Legend = "A (Truth): Drawn line"
    for line in VA:
        (x, y0), (_, y1) = line
        plt.vlines(x, ymin = y0, ymax = y1, colors = 'b', linestyles = 'dashdot', label = Legend)
        Legend = '_nolegend_'

    for line in HA:
        (x0, y), (x1, _) = line
        plt.hlines(y, xmin = x0, xmax = x1, colors = 'b', linestyles = 'dashdot', label = '_nolegend_')
    
    # Plotting B
    coordsB = findCoordinates(B)
    x, y = zip(*coordsB)
    limits = findLimits(x, y, limits)
    plt.plot(x, y, color = 'r', marker = '.', ls = '', label = "B (Guess): Pixels")

    VB, HB = findLines(coordsB)

    Legend = "B (Guess): Drawn line"
    for line in VB:
        (x, y0), (_, y1) = line
        plt.vlines(x, ymin = y0, ymax = y1, colors = 'r', linestyles = 'dashed', label = Legend)
        Legend = '_nolegend_'

    for line in HB:
        (x0, y), (x1, _) = line
        plt.hlines(y, xmin = x0, xmax = x1, colors = 'r', linestyles = 'dashed', label = '_nolegend_')
    
    # Finding difference in vertical and horizontal lines and the metric (value)
    Vrest = set(VA) - set(VB)
    Hrest = set(HA) - set(HB)
    value = str(len(Vrest) + len(Hrest))
    
    # Define axes limits and setting grid
    (x_min, x_max), (y_min, y_max) = limits
    plt.ylim([y_min, y_max])
    plt.xlim([x_min, x_max])
    plt.grid(linestyle='-', linewidth=0.25, which = 'both')

    # Set grid line spacing to 1.
    ax = plt.gca()
    loc = plticker.MultipleLocator(base=1)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)
    ax.set_xticks(np.arange(x_min, x_max + 1))
    ax.set_yticks(np.arange(y_min, y_max + 1))
    ax.set_aspect(1)

    # Title
    plt.title("Added Path length: " + value)
    plt.suptitle(suptitle)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Plot figure
    plt.show()


# Run file (optional)
example = 2
A, B = readExample("AddedPathLengthExamples\\example%d.txt" %example)
print(A.shape)

plot(A, B, f'Example {example}')

# Test on real image
ID = "4Prj3A5sMvSv1sK4u5ihkzlnU"
for segment, method in [("brainstem", "DL"), ("brainstem", "DLB"), ("parotid_merged", "DL"), ("pcm_low", "DL")]:
    pathA = Path(ID, "GT")
    pathB = Path(ID, method)

    OAR_A = OAR_Image(pathA.File, segment)
    OAR_B = OAR_Image(pathB.File, segment)
    
    A = OAR_A.GetArray()
    B = OAR_B.GetArray()

    for z in range(A.shape[0]):
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_min = z
            break
    
    for z in range(A.shape[0])[::-1]:
        if np.sum(A[z,:,:]) > 0 or np.sum(B[z,:,:]):
            z_max = z
            break

    i = (z_max - z_min)//2 + z_min

    plot(A[i], B[i], suptitle = f'OAR: {segment}, Method: {method}, Z: {i}')

# Other
