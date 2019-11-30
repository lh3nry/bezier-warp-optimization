from scene import *

figure_data.remove(mesh2)
figure_data.remove(proj_points)

def intersection_test(direction, origin):
    intersect, U, V = bpatch.intersect(Cx, Cy, Cz, origin, direction)
    # print(intersect)
    # print(origin[None, :])

    if 0 <= U <= 1 and 0 <= V <= 1:
        ray_i = np.concatenate((intersect, origin[None, :]), axis=0)
        X, Y, Z = u.unpack_array_to_tuple(np.array(ray_i))
        ray_plot = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='lines',
            line=dict(color='lightpink', width=2),
            showlegend=False)
        figure_data.append(ray_plot)
        X, Y, Z = u.unpack_array_to_tuple(intersect)
        intersection_markers = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='markers',
            marker=dict(color='aliceblue', size=3),
            showlegend=False)
        figure_data.append(intersection_markers)

    return intersect, (U, V)

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [u.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])


for point in ray_points:
    intersection_test(point, viewpoint)

fig = go.Figure(data=figure_data, layout=layout)
fig.show()