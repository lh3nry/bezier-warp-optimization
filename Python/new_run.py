from scene import *
from plot_utils import intersection_test, intersect_plot

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(proj_plane[:4], ray[0], ray[1]) for ray in rays])

for point in ray_points:
    intersect, uv = intersection_test(point, proj_origin, Cx, Cy, Cz)
    figure_data.extend(intersect_plot(0,0, proj_origin, intersect))

fig = go.Figure(data=figure_data, layout=layout)
fig.show()