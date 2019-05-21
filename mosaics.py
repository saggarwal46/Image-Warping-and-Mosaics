import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

import warpImage as wi
import computeH as cp
import numpy as np
import sys

points1=None
points2 = None
list1 = []
list2 = []

H = None;
fig, ax = plt.subplots(1, 2)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

def argCheck():
    if len(sys.argv) > 4:
        return ((sys.argv[2][-3:] == "jpg" or sys.argv[2][-4:] == "jpeg")
            and (sys.argv[3][-3:] == "jpg" or sys.argv[3][-4:] == "jpeg"))
    else:
        print("Insufficient number of arguments.")

def onclick(event):
    global points1, points2
    if (event.inaxes == ax[0] and onclick.listControl):
        list1.append( [int(event.xdata), int(event.ydata)])
        points1 = np.asarray(list1)
        print((int(event.xdata), int(event.ydata)))
        onclick.listControl = not onclick.listControl
        pointColor = colors[(len(points1) - 1) % len(colors)]
        ax[0].scatter(int(event.xdata), int(event.ydata), c=pointColor, alpha=0.7)
        plt.show()
    elif (event.inaxes == ax[1] and  not onclick.listControl):
        list2.append( [int(event.xdata), int(event.ydata)] )
        points2 = np.asarray(list2)
        print((int(event.xdata), int(event.ydata)))
        pointColor = colors[(len(points2) - 1) % len(colors)]
        ax[1].scatter(int(event.xdata), int(event.ydata), c=pointColor, alpha=0.7)
        onclick.listControl = not onclick.listControl


if __name__ == "__main__":
    if (not argCheck()):
        exit()

    img1 = plt.imread(sys.argv[1] + sys.argv[2], format='jpeg')
    img2 = plt.imread(sys.argv[1] + sys.argv[3], format='jpeg')
    ax[0].imshow(img1)
    ax[1].imshow(img2)

    try:
        points = np.load(sys.argv[1] + sys.argv[4])
        points1 = points[0][:][:].T
        points2 = points[1][:][:].T
    except:
        onclick.listControl = True
        cursor = Cursor(ax[0], horizOn=True, vertOn=True,useblit=False, color='white', linewidth=1)
        cursor1 = Cursor(ax[1], horizOn=True, vertOn=True,useblit=False, color='white', linewidth=1)
        cid = fig.canvas.mpl_connect('button_release_event', onclick)
        plt.show()

    points = np.asarray([points1.T, points2.T])
    np.save(sys.argv[1] + sys.argv[4], points)

    if len(points1) == len(points2) and len(points1) > 3:
        H = cp.computeH(points1, points2)
        (warpIm, mergeIm) = wi.warpImage(img1, img2, H)
        plt.imsave(sys.argv[1] + 'warped.jpg', warpIm)
        plt.imsave(sys.argv[1] + 'merged.jpg', mergeIm)
        ax[0].imshow(warpIm)
        ax[1].imshow(mergeIm)
        plt.show()
