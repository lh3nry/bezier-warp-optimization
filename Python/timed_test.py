from scene import *
# Requires 'stltool.py' from Printrun foudn here: https://raw.githubusercontent.com/kliment/Printrun/master/printrun/stltool.py
from stltool import ray_triangle_intersection, normalize

from plot_utils import intersect_plot
from time import time, perf_counter, process_time

from scipy import stats

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])

ray_dir = ray_points[24]

tri_iteration = 0
# tri_stats = np.array([0.] * len(ray_points)).transpose()
stats_tri = np.zeros((len(ray_points), 1))
i = 0
triangle_time = perf_counter()
for ray in ray_points:
    tri_iteration = perf_counter()
    for tri in patch_tri:
        tri_verts = tuple([Q[i] for i in tri])
        flag, t = ray_triangle_intersection(viewpoint, normalize(ray - viewpoint), tri_verts)
        if flag:
            point = viewpoint + t * normalize(ray - viewpoint)
            # print(flag, t)
            # print(np.concatenate((viewpoint[None, :], point[None, :]), axis=0))
            figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], point[None, :], point_color='maroon'))
        # print("triangle iteration taken", perf_counter() - tri_iteration)
    stats_tri[i] = perf_counter() - tri_iteration
    i += 1
print("triangle time taken ", perf_counter() - triangle_time)

newton_iteration = 0
# newton_stats = np.array([0.] * ray_points)
stats_newton = np.zeros((len(ray_points), 1))
i = 0
estimate = .5 * np.ones((3,1))
newton_time = perf_counter()
for direction in ray_points:
    newton_iteration = perf_counter()
    intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, direction, estimate=estimate)
    # print(intersect, t)
    figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], intersect, point_color='forestgreen'))
    # print("newton iteration taken", perf_counter() - newton_iteration)
    stats_newton[i] = perf_counter() - newton_iteration
    i+=1
print("newton time taken", perf_counter() - newton_time)

fig = go.Figure(data=figure_data, layout=layout)
fig.show()
