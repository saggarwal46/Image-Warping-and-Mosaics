import numpy as np



def computeH(t1, t2):
    """
    Given N >= 4 correlated points from 2 images
    computes the homography parameter from Image 1 to
    Image 2

    Args:
        t1 (ndarray): Points in Image 1 (2xN).
        t2 (ndarray): Corresponding points in Image 2 (2xN).

    Returns:
        ndarray: 3 x 3 homography matrix H.

    """

    n = len(t1)
    A = []
    n -= 1
    while n is not -1:
        A.append([t1[n][0], t1[n][1], 1, 0, 0, 0, -t2[n][0] * t1[n][0], -t2[n][0] * t1[n][1], -t2[n][0]])
        A.append([0, 0, 0, t1[n][0], t1[n][1], 1, -t2[n][1] * t1[n][0], -t2[n][1] * t1[n][1], -t2[n][1]])
        n -= 1
    A=np.asarray(A)
    U,Z,V= np.linalg.svd(A)
    h = V[-1,:]
    H = np.reshape(h,(3,3))
    H /= H[2][2]
    return H
