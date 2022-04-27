import matplotlib.pyplot as plt
import numpy as np

## EPL
EPL = np.linspace(0, 1000, 1000)
GT_Total = [0, 10, 50, 100, 150, 200, 300, 500, 700, 1000]
# Edited_Total = np.linspace(1, 1000, 1)

def lineRatio(EPL, Total):
    return EPL/Total

for t in GT_Total:
    plt.plot(EPL, lineRatio(EPL, t), label = f'Total Lenght = {t}')

plt.legend()
plt.show()

import math
import matplotlib.pyplot as plt
import numpy as np

def f(x, const):
    return const*(x - 3)**2 + math.e**x

x = np.linspace(0, 10, 1000)

for c in [100, 200, 300]:
    plt.plot(x, f(x, c))
plt.show()



lRatio = np.linspace(0, 1, 100)
vRatio = np.linspace(0, 1, 100)
X, Y = np.meshgrid(lRatio, vRatio)

def metric1(lr, vr):
    """LineRatio / VolumeRatio"""
    return lr / vr

def metric2(lr, vr):
    """LineRatio * VolumeRatio"""
    return lr * vr

funcs = [metric1]


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, metric2(X, Y))
fig.show()

fig, axs = plt.subplots(nrows = 1, ncols = len(funcs))
for i, func in enumerate(funcs):
    axs[i] = plt.axes(projection='3d')
    axs[i].set_xlabel('LineRatio [0 ; 1]')
    axs[i].set_ylabel('VolumeRatio [0 ; 1]')
    axs[i].set_zlabel(func.__doc__)
    axs[i].set_title(func.__name__)
    axs[i].plot3D(X, Y, func(X, Y))

plt.show()