import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mptri
from mpl_toolkits.mplot3d import Axes3D
import transforms as xforms


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

view_plane = xforms.translate(view_plane, 0, -25, 0)

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


w_proj = 3
distance = -6

proj_plane = [[ w_proj/2,  0,  w_proj/2],
              [ w_proj/2,  0, -w_proj/2],
              [-w_proj/2,  0,  w_proj/2],
              [-w_proj/2,  0, -w_proj/2],
              [0, distance, 0]];
proj_plane = np.array(proj_plane)

proj_tri = [[0, 1, 3],
			[0, 2, 3]]
proj_tri = np.array(proj_tri)

