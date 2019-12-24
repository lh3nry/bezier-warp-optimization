from scene import *

figure_data.remove(mesh2)
figure_data.remove(proj_points)

def intersection_demo(direction, origin):
    estimate = .5 * np.ones((3,1))
    intersect, demo = bpatch.intersect(Cx, Cy, Cz, origin, direction, estimate=estimate, demo=True)

    return intersect, demo


ray_density = 5
ray_edge = np.linspace(0, 1, ray_density)
x_rays, y_rays = np.meshgrid(ray_edge, ray_edge)
rays = np.stack((x_rays, y_rays))

rays = rays.transpose((2, 1, 0)).reshape(x_rays.size, 2, order='F')

ray_points = np.array(
    [utl.bilinear_sample_plane(view_plane[:4], ray[0], ray[1]) for ray in rays])

ray_dir = ray_points[24]

final_intersect, demo_info = intersection_demo(ray_dir, viewpoint)
fig = go.Figure(data=figure_data, layout=layout)
base_traces = len(fig.data)
base_visibility = [True] * base_traces
visibility = base_visibility + [False] * (2 * len(demo_info))

steps = []

for x in demo_info:
    u, v = np.float64(x[1][0]), np.float64(x[1][1])
    ray_intersect = np.array(viewpoint + x[1][2] * (ray_dir - viewpoint))
    patch_point = bpatch.evaluate_bezier_point(u, v, Cx, Cy, Cz)

    fig.add_trace(go.Scatter3d(
        x=patch_point[0],
        y=patch_point[1],
        z=patch_point[2],
        mode='markers',
        marker=dict(color='aliceblue', size=7)))

    X, Y, Z = utl.unpack_array_to_tuple(
        np.concatenate((ray_intersect[None, :], viewpoint[None, :]), axis=0)
    )
    fig.add_trace(go.Scatter3d(
        x=X,
        y=Y,
        z=Z,
        mode='lines',
        line=dict(color='lightpink', width=5),
        showlegend=False))

    new_vis = visibility[:]
    new_vis[x[0] * 2 + base_traces] = True
    new_vis[x[0] * 2 + base_traces + 1] = True

    steps.append(
        dict(
            method="update",
            args=[{"visible": new_vis},
                  {"title.text": "Iteration %d" % x[0]}]
        )
    )

for i in range(base_traces+2, len(visibility)):
    fig.data[i]['visible'] = False

sliders = [dict (
    steps = steps,
    active = 0,
    currentvalue = {"prefix": "Iteration: "}
)]

fig.update_layout(sliders = sliders, title={"text": "Iteration %d" % 0})

fig.show()

# Uploads plot to chart studio (requires account credentials; check file plotly_set_credentials.py)
ply.plot(fig, filename='iteration_anim', auto_open=True)