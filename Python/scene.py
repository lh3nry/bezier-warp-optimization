import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mptri
from mpl_toolkits.mplot3d import Axes3D
import transforms as xforms
from matplotlib import cm
from matplotlib.colors import ListedColormap as ListCMAP


all_points = np.zeros((1, 3))
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
all_points = np.append(all_points, view_plane, axis=0)

viewpoint = view_plane[4]

print(viewpoint)

upper_left = view_plane[2]
upper_right = view_plane[0]
lower_right = view_plane[1]
lower_left = view_plane[3]

fig = plt.figure(1)
ax = fig.gca(projection='3d')



cmap_name = 'white'
cmap_white = ListCMAP([(1, 1, .5)], cmap_name, 1)
surf = ax.plot_trisurf(view_plane[:4, 0],
                       view_plane[:4, 1],
                       view_plane_triangulated,
                       view_plane[:4, 2], cmap=cmap_white)


w_proj = 3
distance = -6

proj_plane = [[w_proj / 2, 0, w_proj / 2],
              [w_proj / 2, 0, -w_proj / 2],
              [-w_proj / 2, 0, w_proj / 2],
              [-w_proj / 2, 0, -w_proj / 2],
              [0, distance, 0]]
proj_plane = np.array(proj_plane)

proj_tri_triangulated = [[0, 1, 3],
                         [0, 2, 3]]

proj_tri_triangulated = np.array(proj_tri_triangulated)

proj_plane = xforms.rotate(proj_plane, 'x', -50, True)
proj_plane = xforms.translate(proj_plane, 0, -9, -17)
all_points = np.append(all_points, proj_plane, axis=0)

proj_origin = proj_plane[4]

# fig = plt.figure(2)
# ax = fig.gca(projection='3d')
surf = ax.plot_trisurf(proj_plane[:4, 0],
                       proj_plane[:4, 1],
                       proj_tri_triangulated,
                       proj_plane[:4, 2], cmap=cmap_white)


print(all_points)

all_max = np.max(all_points, axis=0)
all_min = np.min(all_points, axis=0)
all_mid = (all_max + all_min) / 2

print(all_max)
print(all_min)
print(all_mid)

max_val = 5
min_val = -max_val


max_range = (all_max - all_min).max() / 2.0

mid_x = all_mid[0] * 0.5
mid_y = all_mid[1] * 0.5
mid_z = all_mid[2] * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.pbaspect = [1, 1, .5]

plt.show()



