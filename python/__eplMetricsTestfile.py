import matplotlib.pyplot as plt
import numpy as np

## EPL
EPL = np.linspace(0, 1000, 1)
GT_Total = [0, 10, 50, 100, 150, 200, 300, 500, 700, 1000]
Edited_Total = np.linspace(1, 1000, 1)

def lineRatio(EPL, Total):
    return EPL/Total

lineRatio()

for t in GT_Total:
    plt.plot(x = EPL, y = lineRatio(EPL, t))

plt.legend()
plt.show()