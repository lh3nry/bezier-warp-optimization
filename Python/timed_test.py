from scene import *
# Requires 'stltool.py' from Printrun foudn here: https://raw.githubusercontent.com/kliment/Printrun/master/printrun/stltool.py
from stltool import ray_triangle_intersection, normalize

from plot_utils import intersect_plot
from time import time, perf_counter, process_time

from scipy.linalg import norm

def rel_error(a, b):
    # assume a is more accurate than b
    if type(a) is np.ndarray and type(b) is np.ndarray:
        a = norm(a)
        b = norm(b)
    return abs((a - b) / a)

def abs_error(a, b):
    if type(a) is np.ndarray and type(b) is np.ndarray:
        a = norm(a)
        b = norm(b)
    return abs(a-b)

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])

tri_iteration = 0
stats_tri = np.zeros((len(ray_points), 4))
i = 0
triangle_time = perf_counter()
for ray in ray_points:
    tri_iteration = perf_counter()
    for tri in patch_tri:
        tri_verts = tuple([Q[i] for i in tri])
        flag, t = ray_triangle_intersection(viewpoint, normalize(ray - viewpoint), tri_verts)
        if flag:
            point = viewpoint + t * normalize(ray - viewpoint)
            figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], point[None, :], point_color='maroon'))
    stats_tri[i,0] = perf_counter() - tri_iteration
    stats_tri[i,1:] = norm(point)
    i += 1
print("triangle time taken ", perf_counter() - triangle_time)

newton_iteration = 0
stats_newton = np.zeros((len(ray_points), 4))
i = 0
estimate = .5 * np.ones((3,1))
newton_time = perf_counter()
for direction in ray_points:
    newton_iteration = perf_counter()
    intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, direction, estimate=estimate)
    figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], intersect, point_color='forestgreen'))
    stats_newton[i,0] = perf_counter() - newton_iteration
    stats_newton[i,1:] = norm(intersect)
    i+=1
print("newton time taken", perf_counter() - newton_time)

relerrs = [rel_error(a,b) for (a,b) in zip(stats_newton[:,1:], stats_tri[:,1:])]
abserrs = [abs_error(a,b) for (a,b) in zip(stats_newton[:,1:], stats_tri[:,1:])]

print("max relative error", max(relerrs), "max absolute error", max(abserrs))

print("average iteration time triangles", np.average(stats_tri[:,0]), "standard deviation", np.std(stats_tri[:,0]))
print("average iteration time newton", np.average(stats_newton[:,0]), "standard deviation", np.std(stats_newton[:,0]))

fig = go.Figure(data=figure_data, layout=layout)
fig.show()
