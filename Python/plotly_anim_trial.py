from scene import *

figure_data.remove(mesh2)
figure_data.remove(proj_points)

def intersection_test(direction, origin):
    # estimate = np.array([[0.5], [0.5], [0.5]])
    estimate = .5 * np.ones((3,1))
    intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, origin, direction, estimate=estimate)
    print(intersect, U, V)
    # print(origin[None, :])
    # intersect_plot(U, V, origin, intersect)
    intersect_plot(0, 0, origin, intersect)

    return intersect, (U, V)

def intersect_plot(U, V, origin, intersect):
    if 0 <= U <= 1 and 0 <= V <= 1:
        ray_i = np.concatenate((intersect, origin[None, :]), axis=0)
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

def intersection_demo(direction, origin):
    estimate = .5 * np.ones((3,1))
    intersect, demo = bpatch.intersect(Cx, Cy, Cz, origin, direction, estimate=estimate, demo=True)
    # intersect_plot(demo[0][1][0], demo[0][1][1], origin, point)
    intersect_plot(0, 0, origin, intersect)

    return intersect, demo

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])

# intersection_test(ray_points[4], viewpoint)

# print(intersection_test(ray_points[12], viewpoint))
# print(intersection_demo(ray_points[12], viewpoint))

# print(intersection_test(ray_points[3], viewpoint))
# print(intersection_test(ray_points[4], viewpoint))
# print(intersection_test(ray_points[9], viewpoint))
# print(intersection_test(ray_points[2], viewpoint))
# print(intersection_test(np.array([2, 25, -2.5]), viewpoint))

# for point in ray_points:
#     intersection_test(point, viewpoint)

final_intersect, demo_info = intersection_demo(ray_points[24], viewpoint)
# for x in demo_info:
    

fig = go.Figure(data=figure_data, layout=layout)
fig.show()