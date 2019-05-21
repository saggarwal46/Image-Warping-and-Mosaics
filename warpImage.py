import numpy as np

def warpImage(inputIm, refIm, H):
    """ Warps Input Image onto the Reference Image using the homography matrix
    H via inverse warp.

    Args:
        inputIm (ndarray): Image to be warped.
        refIm (ndarray): Reference Image.
        H (type): Description of parameter `H`.

    Returns:
        (ndarray, ndarray): Returns the warped version of the input image and
        the warped input image on the reference image.

    """

    H_inv = np.linalg.inv(H)
    inputH, inputW, c = inputIm.shape
    outputH, outputW, c = refIm.shape
    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    cornersi =  [(0,0), (inputH, inputW), (0, inputW), (inputH, 0)]
    cornerso =  [(0,0), (inputH, inputW), (0, inputW), (inputH, 0)]
    for i,j in cornersi:
            x, y, w = np.matmul(H, [j , i, 1])
            x = x/w
            y = y/w
            if x > max_x:
                max_x = int(x)
            if x < min_x:
                min_x = int(x)
            if y > max_y:
                max_y = int(y)
            if y < min_y:
                min_y = int(y)
    warpIm = np.zeros((max_y - min_y,max_x - min_x, 3))
    for i in range(0, max_x - min_x):
        for j in range (0, max_y - min_y):
            x, y, w = np.matmul(H_inv, [i + min_x, j + min_y, 1])
            x = int(x/w)
            y = int(y/w)
            a = 0
            b = 0
            c = 0
            if not (y < 0 or y >= inputH or x < 0 or x >= inputW):
                a, b, c = inputIm[y, x, :]
            warpIm[j, i, :] = [a/255, b/255, c/255]
    oldx = min_x
    oldy = min_y
    oldmx = max_x
    oldmy = max_y
    for i,j in cornerso:
        if j > max_x:
            max_x = int(j)
        if j < min_x:
            min_x = int(j)
        if i > max_y:
            max_y = int(i)
        if i < min_y:
            min_y = int(i)
    mergeIm = np.zeros(((max_y - min_y),(max_x - min_x), 3))
    for i in range(min_x, max_x):
        for j in range (min_y, max_y):
            a = 0
            b = 0
            c = 0
            if not (j < oldy or j >= oldmy or i < oldx or i >= oldmx):
                a, b, c = warpIm[j - oldy, i - oldx, :]
                if a == 0.0 or b == 0.0 or c == 0.0:
                    if not (j < 0 or j >= outputH or i < 0 or i >= outputW):
                        a, b, c = refIm[j, i, :]/255
            else:
                if not (j < 0 or j >= outputH or i < 0 or i >= outputW):
                    a, b, c = refIm[j, i, :]/255
            mergeIm[j - min_y, i- min_x, :] = [a, b, c]

    return (warpIm, mergeIm)
