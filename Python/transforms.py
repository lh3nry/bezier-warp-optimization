import numpy as np


def translate(points, x, y, z):
    for p in points:
        p += np.array([x, y, z])
    return points

