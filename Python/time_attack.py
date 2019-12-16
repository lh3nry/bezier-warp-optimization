from scene import *
from time import time, perf_counter, process_time
from stltool import ray_triangle_intersection, normalize

from utils import generate_rays, rel_error, abs_error

ray_points = generate_rays(view_plane, ray_density=8)

# mesh_sizes = [4,8,16,32,64]#,128]
mesh_sizes = [4,8,16] + list(range(32,65,8))
num_triangles = [0] * len(mesh_sizes)

times_tri = [0] * len(mesh_sizes)
times_newton = [0] * len(mesh_sizes)

results_tri = [[0,0,0]] * len(ray_points)
results_newton = [[0,0,0]] * len(ray_points)

errors = [[0,0,0,0,0,0]] * len(mesh_sizes)

size_index = int(0)
for samples in mesh_sizes:
    Q, T, patch_tri = bpatch.bezier_patch(Cx, Cy, Cz, samples)
    num_triangles[size_index] = len(patch_tri)

    i = 0
    triangle_time = perf_counter()
    for ray in ray_points:
        tri_iteration = perf_counter()
        for tri in patch_tri:
            tri_verts = tuple([Q[i] for i in tri])
            flag, t = ray_triangle_intersection(viewpoint, normalize(ray - viewpoint), tri_verts)
            if flag:
                point = viewpoint + t * normalize(ray - viewpoint)
                results_tri[i] = point
                i += 1
                break
    times_tri[size_index] = perf_counter() - triangle_time
    # print(times_tri[size_index])

    estimate = .5 * np.ones((3, 1))
    i = 0
    newton_time = perf_counter()
    for direction in ray_points:
        newton_iteration = perf_counter()
        intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, direction, estimate=estimate)
        results_newton[i] = intersect
        i += 1
    times_newton[size_index] = perf_counter() - newton_time
    # print(times_newton[size_index])

    rel_errs = [rel_error(a, b) for (a, b) in zip(results_newton, results_tri)]
    abs_errs = [abs_error(a, b) for (a, b) in zip(results_newton, results_tri)]
    errors[size_index] = [max(rel_errs), min(rel_errs), np.average(rel_errs),
                          max(abs_errs), min(abs_errs), np.average(abs_errs)]

    size_index += 1

# print(["{:.5E}".format(x) for x in times_newton])
# print(["{:.5E}".format(x) for x in times_tri])
# print([["{:.5E}, {:.5E}, {:.5E}".format(a,b,c)] for [a,b,c] in errors])

# bar1 = go.Bar(x=["{0} triangles".format(x) for x in num_triangles], y=times_newton,
#                 text=["{0:1.3E} seconds".format(x) for x in times_newton], textposition='auto',
#                 marker=dict(color='#0099ff'),
#                 name='Newton\'s method')
# bar2 = go.Bar(x=["{0} triangles".format(x) for x in num_triangles], y=times_tri,
#                 text=["{0:1.3E} seconds".format(x) for x in times_tri], textposition='auto',
#                 marker=dict(color='#404040'),
#                 name='Ray-Triangle Intersection')

names = ['Max Relative Error', 'Min Relative Error', 'Average Relative Error',
         'Max Absolute Error', 'Min Absolute Error', 'Average Absolute Error']
bar_data = []
for i in [2,5]:
    y_array = np.array(errors)[:,i]
    bar = go.Bar(x=["{0} triangles".format(x) for x in num_triangles], y=y_array,
                    text=["{0:1.3E}".format(x) for x in y_array], textposition='auto',
                    name=names[i])
    bar_data.append(bar)

fig_bars = go.Figure(data=bar_data, layout=go.Layout(width=1000, height=500))
fig_bars.show()

line_newton = go.Scatter(x=["{0} triangles".format(x) for x in num_triangles], y=times_newton,
						 mode='lines+markers',
                         name='Newton\'s method')
line_tri = go.Scatter(x=["{0} triangles".format(x) for x in num_triangles], y=times_tri,
					  mode='lines+markers',
                      name='Ray-Triangle Intersection')

fig_lines = go.Figure(data=[line_newton, line_tri], layout=go.Layout(width=1000, height=500))
fig_lines['layout'].yaxis.update({'title' : 'Time (seconds)'})

fig_lines.show()

# ply.plot(fig_lines, filename='time_attack', auto_open=True)