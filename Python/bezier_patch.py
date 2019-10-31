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

    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    W = lambda w: np.array([[w ** i] for i in range(3, -1, -1)])

    r = np.linspace(0, 1, num_samples)
    s = np.linspace(0, 1, num_samples)

    patch_tensor = patch(r, s, control_x, control_y, control_z)
    print(patch_tensor)
    print(patch_tensor.shape)

    patch_list = patch_tensor.transpose(2,1,0).reshape(num_samples**2, 3, order='F')
    print(patch_list)

    return patch_list, patch_tensor
