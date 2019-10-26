import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mptri
from mpl_toolkits.mplot3d import Axes3D


def translate(points, x, y, z):
    for p in points:
        p += np.array([x, y, z])
    return points


w = 7
distance = -7

view_plane = np.array([[w / 2, 0, w / 2],
                       [w / 2, 0, -w / 2],
                       [-w / 2, 0, w / 2],
                       [-w / 2, 0, -w / 2],
                       [0, distance, 0]])

view_plane_triangulated = [[0, 1, 3],
                           [0, 2, 3]]

# triangulation = mptri.Triangulation(view_plane[:, 0], view_plane[:, 1], view_plane[:, 2],
#                                    view_plane_triangulated)

view_plane = translate(view_plane, 0, -25, 0)

viewpoint = view_plane[4]

print(viewpoint)

upper_left = view_plane[2]
upper_right = view_plane[0]
lower_right = view_plane[1]
lower_left = view_plane[3]

fig = plt.figure()
ax = fig.gca(projection='3d')

surf = ax.plot_trisurf(view_plane[:4, 0], view_plane[:4, 1], view_plane_triangulated, view_plane[:4, 2])

plt.show()
