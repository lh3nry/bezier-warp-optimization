from scene import *
# Requires 'stltool.py' from Printrun foudn here: https://raw.githubusercontent.com/kliment/Printrun/master/printrun/stltool.py
from stltool import ray_triangle_intersection, normalize

import plotly.figure_factory as ff
from plotly.subplots import make_subplots

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
            # figure_data.extend(intersect_plot(0, 0, viewpoint, point, point_color='maroon'))
    stats_tri[i,0] = perf_counter() - tri_iteration
    stats_tri[i,1:] = norm(point)
    i += 1
triangle_time_taken = perf_counter() - triangle_time
print("triangle time taken ", triangle_time_taken)

newton_iteration = 0
stats_newton = np.zeros((len(ray_points), 4))
i = 0
estimate = .5 * np.ones((3,1))
newton_time = perf_counter()
for direction in ray_points:
    newton_iteration = perf_counter()
    intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, direction, estimate=estimate)
    # figure_data.extend(intersect_plot(0, 0, viewpoint, intersect, point_color='forestgreen'))
    stats_newton[i,0] = perf_counter() - newton_iteration
    stats_newton[i,1:] = norm(intersect)
    i+=1
newton_time_taken = perf_counter() - newton_time
print("newton time taken", perf_counter() - newton_time)

relerrs = [rel_error(a,b) for (a,b) in zip(stats_newton[:,1:], stats_tri[:,1:])]
abserrs = [abs_error(a,b) for (a,b) in zip(stats_newton[:,1:], stats_tri[:,1:])]

print("max relative error", max(relerrs), "max absolute error", max(abserrs))

print("average iteration time triangles", np.average(stats_tri[:,0]), "standard deviation", np.std(stats_tri[:,0]))
print("average iteration time newton", np.average(stats_newton[:,0]), "standard deviation", np.std(stats_newton[:,0]))

header_titles = ['','Newton\'s method', 'Ray-Triangle Intersection']
headers = dict(values=header_titles,
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5)

column_newton = [newton_time_taken, np.average(stats_newton[:,0]), max(stats_newton[:,0]), min(stats_newton[:,0]), np.std(stats_newton[:,0])]
column_tri = [triangle_time_taken, np.average(stats_tri[:,0]), max(stats_tri[:,0]), min(stats_tri[:,0]), np.std(stats_tri[:,0])]

column_newton = ["{:.5E}".format(x) for x in column_newton]
column_tri = ["{:.5E}".format(x) for x in column_tri]

fields = ['Total time Taken', 'Average iteration time', 'Max iteration time', 'Min iteration time', 'Iteration standard deviation']
cells = dict(values=[fields,
                     column_newton,
                     column_tri],
             line = dict(color='#7D7F80'),
             fill = dict(color='#EDFAFF'),
             align = ['left'] * 5)


table_rows = [
    header_titles,
    ['Total time Taken', column_newton[0], column_tri[0]],
    ['Average iteration time', column_newton[1], column_tri[1]],
    ['Max iteration time', column_newton[2], column_tri[2]],
    ['Min iteration time', column_newton[3], column_tri[3]],
    ['Iteration standard deviation', column_newton[4], column_tri[4]],
]
# table = go.Table(header=headers, cells=cells)
fig = ff.create_table(table_rows, height_constant=60)

bar1 = go.Bar(x=fields, y=column_newton, xaxis='x2', yaxis='y2',
                marker=dict(color='#0099ff'),
                name='Newton\'s method')
bar2 = go.Bar(x=fields, y=column_tri, xaxis='x2', yaxis='y2',
                marker=dict(color='#404040'),
                name='Ray-Triangle Intersection')

# fig = make_subplots(rows=1, cols=2,
#                     specs=[[{"type" : "table"}, {"type" : "bar"}]])
#
# fig.add_trace(
#     table,
#     row=1, col=1
# )
#
# fig.add_trace(
#     bar1,
#     row=1, col=2
# )
#
# fig.add_trace(
#     bar2,
#     row=1, col=2
# )
# fig = go.Figure(data=[table, trace1, trace2], layout=layout)

# fig['data'].extend(go.Data([bar1, bar2]))
# fig['data'] = (fig['data'], go.Data([bar1, bar2]))
fig.add_trace(bar1)
fig.add_trace(bar2)

# Edit layout for subplots
fig['layout'].xaxis.update({'domain': [0, .5]})
fig.layout.xaxis2 = {}
fig['layout'].xaxis2.update({'domain': [0.6, 1.]})
# The graph's yaxis MUST BE anchored to the graph's xaxis
fig.layout.yaxis2 = {}
fig['layout'].yaxis2.update({'anchor': 'x2'})
fig['layout'].yaxis2.update({'title': 'Time (s)'})
# Update the margins to add a title and see graph x-labels.
fig['layout'].margin.update({'t':50, 'b':100})
fig['layout'].update({'title': 'Timing comparisons'})

# fig = go.Figure(data=figure_data, layout=layout)
fig.show()

# https://plot.ly/python/figure-factory/table/#tables-with-graphs