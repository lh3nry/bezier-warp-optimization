import numpy as np
from scipy.spatial.transform import Rotation as R


def translate(points, x, y, z):
    for p in points:
        p += np.array([x, y, z])
    return points


def rotate(points, axis, theta, degrees):
    r = R.from_euler(axis, theta, degrees)
    points = r.apply(points)
    return points
