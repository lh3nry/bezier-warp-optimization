import numpy as np
import transforms as trfs
from matplotlib.colors import ListedColormap as ListCMAP
import plotly.graph_objs as go
import bezier_patch as bpatch


def unpack_array_to_tuple(np_arr):
    return np_arr[:, 0], np_arr[:, 1], np_arr[:, 2]


def plane_bilinear(corners, u, v):
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
    # interpolated = U @ interpolated

    return U @ interpolated

w = 7
distance = 7

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
distance = 6

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
proj_plane = trfs.translate(proj_plane, 0, 9, -17)

proj_origin = proj_plane[4]

X, Y, Z = unpack_array_to_tuple(view_plane[:4])
I, J, K = unpack_array_to_tuple(view_plane_triangulated)
mesh1 = go.Mesh3d(x=X, y=Y, z=Z,
                  delaunayaxis='y',
                  color='cyan')
A, B, C = unpack_array_to_tuple(proj_plane[:4])
mesh2 = go.Mesh3d(x=A, y=B, z=C, color='lightpink')

figure_data = [mesh1, mesh2]

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
        aspectratio=dict(x=.85, y=1, z=1)
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
Cy = -np.array(Cy)

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

figure_data.append(mesh3)

# print(view_plane[:4])
# print(plane_bilinear(view_plane[:4], 1, 1))
# print(plane_bilinear(view_plane[:4], 0, 0))
# print(plane_bilinear(view_plane[:4], 0, 1))
# print(plane_bilinear(view_plane[:4], 1, 0))

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
# print(x_rays)
# print(y_rays)

rays = np.stack((x_rays, y_rays))
# print(rays)

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')
# for ray in rays:
#     print(plane_bilinear(view_plane[:4], ray[0], ray[1]))

ray_points = np.array(
    [plane_bilinear(proj_plane[:4], ray[0], ray[1]) for ray in rays])
# print(ray_points)

X, Y, Z = unpack_array_to_tuple(np.array(view_plane))
view_points = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')

X, Y, Z = unpack_array_to_tuple(np.array(proj_plane))
proj_points = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')

figure_data.append(proj_points)
figure_data.append(view_points)

# intersect = bpatch.intersect(Cx, Cy, Cz, proj_origin, ray_points[0])
# ray_i = np.concatenate((intersect, proj_origin[None,:]), axis=0)
# X, Y, Z = unpack_array_to_tuple(np.array(ray_i))
# ray_plot = go.Scatter3d(x=X, y=Y, z=Z, mode='lines', line=dict(width=2))
# figure_data.append(ray_plot)


for point in ray_points:
    intersect = bpatch.intersect(Cx, Cy, Cz, proj_origin, point)
    # print(intersect)
    # print(intersect.shape)
    # print(proj_origin)
    # print(proj_origin.shape)
    # ray_i = np.array([point, proj_origin])
    # ray_i = np.array([bpatch.intersect(Cx, Cy, Cz, proj_origin, point), proj_origin])
    ray_i = np.concatenate((intersect, proj_origin[None,:]), axis=0)
    # print(ray_i)
    X, Y, Z = unpack_array_to_tuple(np.array(ray_i))
    ray_plot = go.Scatter3d(x=X, y=Y, z=Z, mode='lines', line=dict(width=2))
    # ray_plot = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')
    figure_data.append(ray_plot)

fig = go.Figure(data=figure_data, layout=layout)
fig.show()
