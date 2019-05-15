import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import warpImage as wi
import computeH as cp

points1=None
points2 = None
list1 = []
list2 = []

H = None;
fig, ax = plt.subplots(1, 2)
def onclick(event):
    global points1, points2
    if (event.inaxes == ax[0] and onclick.listControl):
        list1.append( [int(event.xdata), int(event.ydata)])
        points1 = np.asarray(list1)
        print((int(event.xdata), int(event.ydata)))
        onclick.listControl = not onclick.listControl
    elif (event.inaxes == ax[1] and  not onclick.listControl):
        list2.append( [int(event.xdata), int(event.ydata)] )
        points2 = np.asarray(list2)
        print((int(event.xdata), int(event.ydata)))
        onclick.listControl = not onclick.listControl


img1 = plt.imread('crop1.jpg', format='jpeg')
img2 = plt.imread('crop2.jpg', format='jpeg')
ax[0].imshow(img1)
ax[1].imshow(img2)

try:
    points = np.load('points.npy')
    points1 = points[0][:][:].T
    points2 = points[1][:][:].T
except:
    onclick.listControl = True
    cursor = Cursor(ax[0], horizOn=True, vertOn=True,useblit=False, color='white', linewidth=1)
    cursor1 = Cursor(ax[1], horizOn=True, vertOn=True,useblit=False, color='white', linewidth=1)
    cid = fig.canvas.mpl_connect('button_release_event', onclick)
    plt.show()

points = np.asarray([points1.T, points2.T])
np.save('points.npy', points)

if len(points1) == len(points2) and len(points1) > 3:
    H = cp.computeH(points1, points2)
    (warpIm, mergeIm) = wi.warpImage(img1, img2, H)
    plt.imsave('q1w.jpg', warpIm)
    plt.imsave('q1m.jpg', mergeIm)
    ax[0].imshow(warpIm)
    ax[1].imshow(mergeIm)
    plt.show()
