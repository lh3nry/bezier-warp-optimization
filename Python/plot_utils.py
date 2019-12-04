import bezier_patch as bpatch
import plotly.graph_objs as go
import numpy as np
import utils as utl


def intersection_test(direction, origin, Cx, Cy, Cz):
    # estimate = np.array([[0.5], [0.5], [0.5]])
    estimate = .5 * np.ones((3,1))
    intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, origin, direction, estimate=estimate)
    print(intersect, U, V)
    # print(origin[None, :])
    # intersect_plot(U, V, origin, intersect)
    # intersect_plot(0, 0, origin[None, :], intersect)

    return intersect, (U, V)

def intersect_plot(U, V, origin, intersect, line_color='lightpink', point_color='aliceblue'):
    figure_data = []
    if 0 <= U <= 1 and 0 <= V <= 1:
        ray_i = np.concatenate((intersect[None, :], origin[None, :]), axis=0)
        X, Y, Z = utl.unpack_array_to_tuple(np.array(ray_i))
        ray_plot = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='lines',
            line=dict(color=line_color, width=3),
            showlegend=False)
        figure_data.append(ray_plot)
        X, Y, Z = utl.unpack_array_to_tuple(intersect[None, :])
        intersection_markers = go.Scatter3d(
            x=X, y=Y, z=Z,
            mode='markers',
            marker=dict(color=point_color, size=4),
            showlegend=False)
        figure_data.append(intersection_markers)
    return figure_data

# def intersection_demo(direction, origin, Cx, Cy, Cz):
#     estimate = .5 * np.ones((3,1))
#     intersect, demo = bpatch.intersect(Cx, Cy, Cz, origin, direction, estimate=estimate, demo=True)
#     # intersect_plot(demo[0][1][0], demo[0][1][1], origin, point)
#     # intersect_plot(0, 0, origin, intersect)
#
#     return intersect, demo