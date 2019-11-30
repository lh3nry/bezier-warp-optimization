import numpy as np

basis = [[-1,  3, -3, 1],
         [ 3, -6,  3, 0],
         [-3,  3,  0, 0],
         [ 1,  0,  0, 0]]


def patch(u, v, cx, cy, cz):
    num_samples = len(v)        # TODO: Assert |v| = |u|
    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    W = lambda w: np.array([[w ** i] for i in range(3, -1, -1)])

    left = U(u).transpose() @ basis
    right = basis @ W(v).reshape(4, num_samples)

    return np.array([
        left @ cx @ right,
        left @ cy @ right,
        left @ cz @ right
    ])


def bezier_patch(control_x, control_y, control_z, num_samples):
    np.set_printoptions(precision=3)

    r = np.linspace(0, 1, num_samples)
    s = np.linspace(0, 1, num_samples)

    patch_tensor = patch(r, s, control_x, control_y, control_z)
    # print(patch_tensor)
    # print(patch_tensor.shape)

    samples_squared = num_samples**2
    patch_list = patch_tensor.transpose((2, 1, 0)).reshape(samples_squared, 3, order='F')
    # print(patch_list)

    triangulation = []
    for i in range(samples_squared - num_samples - 1):
        if i % num_samples != num_samples - 1:
            triangulation.append([i, i+1, i+num_samples])
            triangulation.append([i+1, i+num_samples+1, i+num_samples])

    return patch_list, patch_tensor, triangulation


def intersect(control_x, control_y, control_z, ray_origin, ray_point, estimate = np.zeros((3, 1)), demo = False):
    tol = 1e-12
    max_itr = 10
    t_max = 10

    # Pre-compute constant matrices
    Ax = basis @ control_x @ basis
    Ay = basis @ control_y @ basis
    Az = basis @ control_z @ basis

    ray_direction = ray_point - ray_origin

    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    V = lambda v: np.array([[v ** i] for i in range(3, -1, -1)])
    evaluate_bezier = lambda u, v: np.array([U(u) @ Ax @ V(v), U(u) @ Ay @ V(v), U(u) @ Az @ V(v)])

    # Derivatives of parameter degree vectors
    Udu = lambda u: np.array([3*u**2, 2*u, 1, 0])
    Vdv = lambda v: np.array([[3*v**2],
                              [2*v],
                              [1],
                              [0]    ])

    jacobian = lambda u, v, t: np.array([
        [np.float64(Udu(u) @ Ax @ V(v)), np.float64(U(u) @ Ax @ Vdv(v)), -ray_direction[0]],
        [np.float64(Udu(u) @ Ay @ V(v)), np.float64(U(u) @ Ay @ Vdv(v)), -ray_direction[1]],
        [np.float64(Udu(u) @ Az @ V(v)), np.float64(U(u) @ Az @ Vdv(v)), -ray_direction[2]],
    ])
    J = lambda x: jacobian(np.float64(x[0]), np.float64(x[1]), np.float64(x[2]))

    objective = lambda u, v, t: evaluate_bezier(u, v) - ray_origin.reshape(-1,1) - t * ray_direction.reshape(-1,1)
    F = lambda x: objective(np.float64(x[0]), np.float64(x[1]), np.float64(x[2]))

    itr_count = 0
    newton_update = np.ones((3, 1))
    x_i = estimate
    if demo:
        demo_storage = []
        while np.abs(x_i[2]) < t_max and (newton_update[0] >= tol or newton_update[1] >= tol or newton_update[2] >= tol) and itr_count <= max_itr :
            demo_storage.append((itr_count, x_i))
            print((itr_count, x_i))
            newton_update = - np.linalg.solve(J(x_i), F(x_i))
            x_i += newton_update
            itr_count += 1
    else:
        while np.abs(x_i[2]) < t_max and (newton_update[0] >= tol or newton_update[1] >= tol or newton_update[2] >= tol) and itr_count <= max_itr :
            print((itr_count, x_i))
            newton_update = - np.linalg.solve(J(x_i), F(x_i))
            x_i += newton_update
            itr_count += 1

    u, v, t = np.float64(x_i[0]), np.float64(x_i[1]), np.float64(x_i[2])

    ray_eval = np.array(ray_origin + t * ray_direction)
    # intersection_point = evaluate_bezier(u, v).transpose()
    intersection_point = ray_eval[None, :]

    if demo:
        return intersection_point, demo_storage
    return intersection_point, u, v, t
