from scene import *
from plot_utils import intersection_test, intersect_plot
from utils import generate_rays

ray_density = 5

ray_points = generate_rays(proj_plane, ray_density)

for point in ray_points:
    intersect, uv = intersection_test(point, proj_origin, Cx, Cy, Cz)
    figure_data.extend(intersect_plot(0,0, proj_origin, intersect))

fig = go.Figure(data=figure_data, layout=layout)
fig.show()