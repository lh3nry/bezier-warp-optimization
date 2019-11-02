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


def intersect(control_x, control_y, control_z, ray_origin, ray_direction):
    tol = 1e-7
    max_itr = 10
    t_max = 15
    Ax = basis @ control_x @ basis
    Ay = basis @ control_y @ basis
    Az = basis @ control_z @ basis

    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    Udu = lambda u: np.array([3*u**2, 2*u, 1, 0])
    V = lambda v: np.array([[v ** i] for i in range(3, -1, -1)])
    Vdv = lambda v: np.array([[3*v**2], [2*v], [1], [0]])

    # print(V(1))
    # print(Vdv(1))

    evaluate_bezier = lambda u, v: np.array([U(u) @ Ax @ V(v), U(u) @ Ay @ V(v), U(u) @ Az @ V(v)])

    print(evaluate_bezier(0, 0))

    jacobian = lambda u, v, t: np.array([
        [np.float(Udu(u) @ Ax @ V(v)), np.float(U(u) @ Ax @ Vdv(v)), -ray_direction[0]],
        [np.float(Udu(u) @ Ay @ V(v)), np.float(U(u) @ Ay @ Vdv(v)), -ray_direction[1]],
        [np.float(Udu(u) @ Az @ V(v)), np.float(U(u) @ Az @ Vdv(v)), -ray_direction[2]],
    ])
    J = lambda x: jacobian(np.float(x[0]), np.float(x[1]), np.float(x[2]))

    objective = lambda u, v, t: evaluate_bezier(u, v) - ray_origin.reshape(-1,1) - t * ray_direction.reshape(-1,1)
    F = lambda x: objective(np.float(x[0]), np.float(x[1]), np.float(x[2]))

    # while abs(xx(3)) < t_max & & (newt_update(1) >= tol | | newt_update(2) >= tol) & & it_count <= it_max
    J_inv = np.linalg.inv(jacobian(0, 0, 0))
    # print(jacobian(0, 0, 0))
    # print(J_inv)
    newton_update = np.ones((3, 1)) * (tol + 1)
    # print(newton_update)
    # print(J_inv @ objective(0, 0, 0))
    # print((J_inv @ objective(0, 0, 0)).shape)
    # print(J_inv.shape)
    # print(objective(0, 0, 0).shape)
    # print(objective(0, 0, 0))
    # print(evaluate_bezier(0,0) - ray_origin.reshape(-1,1))
    # print(J(newton_update))

    itr_count = 1
    x_i = np.zeros((3, 1))
    while np.abs(x_i[2]) < t_max and (newton_update[0] >= tol or newton_update[1] >= tol) and itr_count <= max_itr :
        newton_update = -np.linalg.inv(J(x_i)) @ F(x_i)
        x_i += newton_update
        print(itr_count)
        print(x_i)
        print(newton_update)
        itr_count += 1