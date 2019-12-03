from scene import *
from stltool import ray_triangle_intersection, normalize

from plotly_anim_trial import intersect_plot

# print(patch_tri)
# print(Q)

def ray_intersect_triangle(p0, p1, triangle):
    # Tests if a ray starting at point p0, in the direction
    # p1 - p0, will intersect with the triangle.
    #
    # arguments:
    # p0, p1: numpy.ndarray, both with shape (3,) for x, y, z.
    # triangle: numpy.ndarray, shaped (3,3), with each row
    #     representing a vertex and three columns for x, y, z.
    #
    # returns:
    #    0.0 if ray does not intersect triangle,
    #    1.0 if it will intersect the triangle,
    #    2.0 if starting point lies in the triangle.
    v0, v1, v2 = triangle
    u = v1 - v0
    v = v2 - v0
    normal = np.cross(u, v)
    b = np.inner(normal, p1 - p0)
    a = np.inner(normal, v0 - p0)

    # Here is the main difference with the code in the link.
    # Instead of returning if the ray is in the plane of the
    # triangle, we set rI, the parameter at which the ray
    # intersects the plane of the triangle, to zero so that
    # we can later check if the starting point of the ray
    # lies on the triangle. This is important for checking
    # if a point is inside a polygon or not.

    if b == 0.0:
        # ray is parallel to the plane
        if a != 0.0:
            # ray is outside but parallel to the plane
            return 0, None
        else:
            # ray is parallel and lies in the plane
            rI = 0.0
    else:
        rI = a / b
    if rI < 0.0:
        return 0, None
    w = p0 + rI * (p1 - p0) - v0
    denom = np.inner(u, v) * np.inner(u, v) - np.inner(u, u) * np.inner(v, v)
    si = (np.inner(u, v) * np.inner(w, v) - np.inner(v, v) * np.inner(w, u)) / denom

    if (si < 0.0) or (si > 1.0):
        return 0, None
    ti = (np.inner(u, v) * np.inner(w, u) -
          np.inner(u, u) * np.inner(w, v)) / denom

    if (ti < 0.0) or (si + ti > 1.0):
        return 0, None
    if rI == 0.0:
        # point 0 lies ON the triangle. If checking for
        # point inside polygon, return 2 so that the loop
        # over triangles can stop, because it is on the
        # polygon, thus inside.
        return 2, rI
    return 1, rI

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
        intersect_plot(0, 0, viewpoint[None, :], point[None, :])

# for tri in patch_tri:
#     tri_verts = tuple([Q[i] for i in tri])
#     inters, t = ray_intersect_triangle(viewpoint, ray_dir, tri_verts)
#     if inters > 0:
#         print(viewpoint + t * ray_dir, t)
        # print(viewpoint + t * ray_dir)

estimate = .5 * np.ones((3,1))
intersect, U, V, t = bpatch.intersect(Cx, Cy, Cz, viewpoint, ray_dir, estimate=estimate)
print(intersect, t)
intersect_plot(0, 0, viewpoint[None, :], intersect)

fig = go.Figure(data=figure_data, layout=layout)
fig.show()
