import plotly.graph_objects as go
import numpy as np

from plotly.offline import iplot
import plotly.figure_factory as FF
import plotly.graph_objs as go
from scipy.spatial import Delaunay
import transforms as xforms


def unpack_array_to_tuple(np_arr):
    # simplices is a numpy array defining the simplices of the triangularization
    # returns the lists of indices i, j, k

    # return ([triplet[c] for triplet in simplices] for c in range(3))
    return np_arr[:, 0], np_arr[:, 1], np_arr[:, 2]


u = np.linspace(0, 2 * np.pi, 20)
v = np.linspace(0, 2 * np.pi, 20)
u, v = np.meshgrid(u, v)
u = u.flatten()
v = v.flatten()

x = (3 + (np.cos(v))) * np.cos(u)
y = (3 + (np.cos(v))) * np.sin(u)
z = np.sin(v)

points2D = np.vstack([u, v]).T
tri = Delaunay(points2D)
simplices = tri.simplices

layout = go.Layout(
    width=1024,
    height=1024,
    scene=dict(camera=dict(eye=dict(x=1.15, y=1.15, z=0.8)),  # the default values are 1.25, 1.25, 1.25
               xaxis=dict(),
               yaxis=dict(),
               zaxis=dict(),
               aspectmode='manual',  # this string can be 'data', 'cube', 'auto', 'manual'
               # a custom aspectratio is defined as follows:
               aspectratio=dict(x=1, y=1, z=1)
               )
)

I, J, K = unpack_array_to_tuple(simplices)
data1 = go.Mesh3d(x=x, y=y, z=z,
                  i=I, j=J, k=K)

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
proj_plane = xforms.translate(proj_plane, 0, 9, 17)

X, Y, Z = unpack_array_to_tuple(proj_plane[:4])
data2 = go.Mesh3d(x=X, y=Y, z=Z)

data = [data1, data2]

fig = go.Figure(data=data)
fig.show()
