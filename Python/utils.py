import numpy as np
from scipy.linalg import norm


def unpack_array_to_tuple(np_arr):
    return np_arr[:, 0], np_arr[:, 1], np_arr[:, 2]


def bilinear_sample_plane(corners, u, v):
    G = np.array([
        [corners[3, 0], corners[2, 0]],
        [corners[1, 0], corners[0, 0]],
        [corners[3, 1], corners[2, 1]],
        [corners[1, 1], corners[0, 1]],
        [corners[3, 2], corners[2, 2]],
        [corners[1, 2], corners[0, 2]]
    ])

    U = np.array([1-u, u])
    V = np.array([[1-v], [v]])

    interpolated = (G @ V).reshape(2, 3, order='F')

    return U @ interpolated


def generate_rays(plane, ray_density = 5):
    global ray_points
    ray_edge = np.linspace(0, 1, ray_density)
    x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
    rays = np.stack((x_rays, y_rays))
    rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')
    return np.array(
        [bilinear_sample_plane(plane[:4], ray[0], ray[1]) for ray in rays])


def rel_error(a, b):
    # assume a is more accurate than b
    if type(a) is np.ndarray and type(b) is np.ndarray:
        a = norm(a)
        b = norm(b)
    return abs((a - b) / a)

def abs_error(a, b):
    if type(a) is np.ndarray and type(b) is np.ndarray:
        a = norm(a)
        b = norm(b)
    return abs(a-b)

