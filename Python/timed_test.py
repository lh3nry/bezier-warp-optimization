from scene import *
from stltool import ray_triangle_intersection, normalize

from plot_utils import intersect_plot

ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])

ray_dir = ray_points[24]

for tri in patch_tri:
    tri_verts = tuple([Q[i] for i in tri])
    flag, t = ray_triangle_intersection(viewpoint, normalize(ray_dir - viewpoint), tri_verts)
    if flag:
        point = viewpoint + t * normalize(ray_dir - viewpoint)
        print(flag, t)
        # print(np.concatenate((viewpoint[None, :], point[None, :]), axis=0))
        figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], point[None, :]))

# for tri in patch_tri:
#     tri_verts = tuple([Q[i] for i in tri])
#     inters, t = ray_intersect_triangle(viewpoint, ray_dir, tri_verts)
#     if inters > 0:
#         print(viewpoint + t * ray_dir, t)
        # print(viewpoint + t * ray_dir)

estimate = .5 * np.ones((3,1))
intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, ray_dir, estimate=estimate)
print(intersect, t)
figure_data.extend(intersect_plot(0, 0, viewpoint[None, :], intersect))

fig = go.Figure(data=figure_data, layout=layout)
fig.show()
