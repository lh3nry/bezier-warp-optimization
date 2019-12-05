from scene import *
from time import time, perf_counter, process_time
from stltool import ray_triangle_intersection, normalize

from utils import generate_rays, rel_error, abs_error

ray_points = generate_rays(view_plane)

mesh_sizes = [4,8,16,32,64]#,128]
num_triangles = [0] * len(mesh_sizes)

times_tri = [0] * len(mesh_sizes)
times_newton = [0] * len(mesh_sizes)

results_tri = [[0,0,0]] * len(ray_points)
results_newton = [[0,0,0]] * len(ray_points)

errors = [[0,0,0]] * len(mesh_sizes)
# errors_newton = [0,0,0] * len(mesh_sizes)

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
    errors[size_index] = [max(rel_errs), min(rel_errs), np.average(rel_errs)]


    size_index += 1

print(["{:.5E}".format(x) for x in times_newton])
print(["{:.5E}".format(x) for x in times_tri])
print([["{:.5E}, {:.5E}, {:.5E}".format(a,b,c)] for [a,b,c] in errors])