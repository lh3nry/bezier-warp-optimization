import numpy as np
import transforms as trfs
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

upper_left = view_plane[2]
upper_right = view_plane[0]
lower_right = view_plane[1]
lower_left = view_plane[3]

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
mesh1 = go.Mesh3d(x=X, y=Y, z=Z,
                  delaunayaxis='y',
                  color='cyan')
A, B, C = unpack_array_to_tuple(proj_plane[:4])
mesh2 = go.Mesh3d(x=A, y=B, z=C, color='lightpink')
figure_data = [mesh1, mesh2]

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
# bez_scatter = go.Scatter3d(x=Px, y=Py, z=Pz, mode='markers')
figure_data.append(mesh3)

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [plane_bilinear(proj_plane[:4], ray[0], ray[1]) for ray in rays])

X, Y, Z = unpack_array_to_tuple(np.array(view_plane))
view_points = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')

X, Y, Z = unpack_array_to_tuple(np.array(proj_plane))
proj_points = go.Scatter3d(x=X, y=Y, z=Z, mode='markers')

figure_data.append(proj_points)
figure_data.append(view_points)

for point in ray_points:
    intersect = bpatch.intersect(Cx, Cy, Cz, proj_origin, point)
    ray_i = np.concatenate((intersect, proj_origin[None,:]), axis=0)
    X, Y, Z = unpack_array_to_tuple(np.array(ray_i))
    ray_plot = go.Scatter3d(x=X, y=Y, z=Z, mode='lines', line=dict(color='lightpink', width=2), showlegend=False)
    figure_data.append(ray_plot)
    X, Y, Z = unpack_array_to_tuple(intersect)
    intersection_markers = go.Scatter3d(x=X, y=Y, z=Z, 
                                        mode='markers', marker=dict( color='aliceblue', size=3), showlegend=False)
    figure_data.append(intersection_markers)

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
fig = go.Figure(data=figure_data, layout=layout)
fig.show()
