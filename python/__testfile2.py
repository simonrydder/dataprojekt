from time import process_time as pt
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt
import numpy as np
from functools import lru_cache
from DataPreparation2 import OAR_Image
from DataReader2 import Path


def readExample(file):
    array = []
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            values = [int(c) for c in line.split()]
            array.append(values)
    
    return np.array(array)


def findPoints(A):
    return {(x, y) for y, x in zip(*np.nonzero(A))}


def findResultingPoints(gtPoints, guessPoints, tol = 0):
    """
    pA is the points from ground truth.
    pB is the points from the guess.
    """        
    
    def findValidGuessPoints(tol = 0):
        nonlocal gtPoints, guessPoints

        @lru_cache
        def isValid(x, y, tol = 0):
            
            if tol == 0:
                return (x, y) in gtPoints
            
            for dx, dy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
                if isValid(x + dx, y + dy, tol - 1):
                    return True
            
            return False

        return {(x, y) for x, y in guessPoints if isValid(x, y, tol)}


    def findValidGTPoints(tol = 0):
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

    pRes = findValidGuessPoints(tol) | findValidGTPoints(tol)

    return pRes


def findLines(coordinates):
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


def plotPoints(points, col = 'b', mark = 'o'):
    x, y = zip(*points)
    y = [-y_ for y_ in y]
    plt.plot(x, y, color = col, marker = mark, ls = '')


def plotLines(lines, color = 'b', style = 'dashdot', width = 1):
    for (x0, y0), (x1, y1) in lines:
        if x0 == x1:
            plt.vlines(x0, ymin = -y0, ymax = -y1, colors = color, ls = style, lw = width)
        else:
            plt.hlines(-y0, xmin = x0, xmax = x1, colors = color, ls = style, lw = width)


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

tol = 1
seg = 'lips'
sli = 80
A = readExample(f'EPL_examples\\{seg}A{sli}.txt')   # GT
B = readExample(f'EPL_examples\\{seg}B{sli}.txt')   # Guess

pA = findPoints(A)
pB = findPoints(B)

vGuess, hGuess = findLines(pB)
vTrue, hTrue = findLines(pA)
plotLines(vGuess | hGuess)

vRes, hRes = findLines(findResultingPoints(pA, pB, tol))

vEPL = vRes - vGuess
hEPL = hRes - hGuess
plotLines(vEPL | hEPL, color = 'lime', style = 'dashed', width = 2)
plotLines(vTrue | hTrue, color = 'k', style = 'dotted')
plotPoints(pA, col = 'k', mark = '.')
plot(len(A[0]), len(A))


def generateNewExample(segment, ID = '4Prj3A5sMvSv1sK4u5ihkzlnU', Date = '20190129'):
    P1 = Path(ID, Date, 'GT')
    P2 = Path(ID, Date, 'DL')

    Segment = segment
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

    print(A.shape, B.shape)
    A_ = A[x_min:x_max, y_min:y_max]
    B_ = B[x_min:x_max, y_min:y_max]
    print(A)

    with open(f'EPL_examples\\{Segment}A{Slice}.txt', 'w') as f:
        for row in A_[::-1]:
            f.write(' '.join([str(n) for n in list(row)]) + '\n')

    with open(f'EPL_examples\\{Segment}B{Slice}.txt', 'w') as f:
        for row in B_[::-1]:
            f.write(' '.join([str(n) for n in list(row)]) + '\n')

generateNewExample('lips')