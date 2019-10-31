import numpy as np
import transforms as trfs
from matplotlib.colors import ListedColormap as ListCMAP
import plotly.graph_objs as go
import bezier_patch as bpatch


def unpack_array_to_tuple(np_arr):
    return np_arr[:, 0], np_arr[:, 1], np_arr[:, 2]


w = 7
distance = -7

view_plane = np.array([[w / 2, 0, w / 2],
                       [w / 2, 0, -w / 2],
                       [-w / 2, 0, w / 2],
                       [-w / 2, 0, -w / 2],
                       [0, distance, 0]])

view_plane_triangulated = [[0, 1, 3],
                           [0, 2, 3]]
view_plane_triangulated = np.array(view_plane_triangulated)

view_plane = trfs.translate(view_plane, 0, 25, 0)

viewpoint = view_plane[4]

# print(viewpoint)

upper_left = view_plane[2]
upper_right = view_plane[0]
lower_right = view_plane[1]
lower_left = view_plane[3]

cmap_name = 'white'
cmap_white = ListCMAP([(1, 1, .5)], cmap_name, 1)

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

proj_plane = trfs.rotate(proj_plane, 'x', -50, True)
proj_plane = trfs.translate(proj_plane, 0, -9, -17)

proj_origin = proj_plane[4]

X, Y, Z = unpack_array_to_tuple(view_plane[:4])
I, J, K = unpack_array_to_tuple(view_plane_triangulated)
mesh1 = go.Mesh3d(x=X, y=Y, z=Z,
                  delaunayaxis='y',
                  color='cyan')
A, B, C = unpack_array_to_tuple(proj_plane[:4])
mesh2 = go.Mesh3d(x=A, y=B, z=C, color='lightpink')

test = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')

layout = go.Layout(
    width=1024,
    height=1024,
    scene=dict(
        camera=dict(
            eye=dict(x=1.15, y=1.15, z=0.8)),  # the default values are 1.25, 1.25, 1.25
        xaxis=dict(),
        yaxis=dict(),
        zaxis=dict(),
        aspectmode='manual',  # this string can be 'data', 'cube', 'auto', 'manual'
        # a custom aspectratio is defined as follows:
        aspectratio=dict(x=1, y=1, z=1)
    )
)

Cx = [[-15, -15, -15, -15],
      [ -5,  -5,  -5,  -5],
      [  5,   5,   5,   5],
      [ 15,  15,  15,  15]]
Cx = np.array(Cx)

Cy = [[0, 5, 5, 0],
      [5, 5, 5, 5],
      [5, 5, 5, 5],
      [0, 5, 5, 0]]
Cy = np.array(Cy)

Cz = [[15, 5, -5, -15],
      [15, 5, -5, -15],
      [15, 5, -5, -15],
      [15, 5, -5, -15]]
Cz = np.array(Cz)

Q, T, patch_tri = bpatch.bezier_patch(Cx, Cy, Cz, 15)

Px, Py, Pz = unpack_array_to_tuple(Q)
I, J, K = unpack_array_to_tuple(np.array(patch_tri))
mesh3 = go.Mesh3d(x=Px, y=Py, z=Pz, i=I, j=J, k=K)
bez_scatter = go.Scatter3d(x=Px, y=Py, z=Pz, mode='markers')

fig = go.Figure(data=[
    mesh1,
    mesh2,
    mesh3  # , bez_scatter
    ], layout=layout)
fig.show()
