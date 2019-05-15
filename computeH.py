import numpy as np

def computeH(t1, t2):
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
