import numpy as np


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