# import scene as sc
from scene import *
# import numpy as np
# import utils as u

def intersection_test(direction, origin):
    intersect, U, V,  t = bpatch.intersect(Cx, Cy, Cz, origin, direction)
    # assert(0 <= U <= 1)
    # assert(0 <= V <= 1)

    intersect_plot(U, V, origin[None, :], intersect)

def intersect_plot(U, V, origin, intersect):
    if 0 <= U <= 1 and 0 <= V <= 1:
        ray_i = np.concatenate((intersect, origin), axis=0)
        # X, Y, Z = u.unpack_array_to_tuple(np.array(ray_i))
        X, Y, Z = utl.unpack_array_to_tuple(np.array(ray_i))
        ray_plot = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='lines',
            line=dict(color='lightpink', width=2),
            showlegend=False)
        figure_data.append(ray_plot)
        X, Y, Z = utl.unpack_array_to_tuple(intersect)
        intersection_markers = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='markers',
            marker=dict(color='aliceblue', size=3),
            showlegend=False)
        figure_data.append(intersection_markers)

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(proj_plane[:4], ray[0], ray[1]) for ray in rays])

for point in ray_points:
    intersection_test(point, proj_origin)

fig = go.Figure(data=figure_data, layout=layout)
fig.show()