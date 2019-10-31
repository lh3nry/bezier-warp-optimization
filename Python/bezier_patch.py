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

    # print(control_x.shape)
    # print(control_y.shape)
    # print(control_z.shape)
    np.set_printoptions(precision=3)

    basis = [[-1,  3, -3, 1],
             [ 3, -6,  3, 0],
             [-3,  3,  0, 0],
             [ 1,  0,  0, 0]]
    basis = np.array(basis)
    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    W = lambda w: np.array([[w ** i] for i in range(3, -1, -1)])

    # patch = lambda u,w: np.array([
    #     U(u) @ basis @ control_x @ basis @ W(w)
    #     # ,
    #     # U(u) @ basis @ control_y @ basis @ W(w),
    #     # U(u) @ basis @ control_z @ basis @ W(w)
    # ])

    r = np.linspace(0, 1, num_samples)#[np.newaxis,:]
    s = np.linspace(0, 1, num_samples)

    u, v = np.meshgrid(r, s, sparse=True)

    # print(u)
    # print(v)
    #
    # patch(u, v)

    # patch(r, s)

    # print(U(r).transpose())
    # print(U(r).shape)
    # print(U(r).transpose() @ basis)
    # print(U(r).transpose() @ basis @ control_x @ basis)

    # print(basis @ W(s))
    # print(W(s))
    # print(W(s).shape)
    # print(W(s).transpose())
    # print(s)
    # print(s[None, :].transpose())
    #
    # print(W(s))
    # print(W(s).shape)
    # WW = W(s).reshape(4, num_samples)
    # print(WW)
    # print(WW.shape)

    # print(U(r).transpose() @ basis @ control_x @ basis @ WW)
    patch_points = patch(r,s, control_x, control_y, control_z)
    print(patch_points)
    print(patch_points.shape)

    # return U