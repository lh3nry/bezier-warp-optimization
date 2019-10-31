def bezier_patch(control_x, control_y, control_z, sample_density):
    import numpy as np

    # print(control_x.shape)
    # print(control_y.shape)
    # print(control_z.shape)

    basis = [[-1,  3, -3, 1],
             [ 3, -6,  3, 0],
             [-3,  3,  0, 0],
             [ 1,  0,  0, 0]]
    basis = np.array(basis)
    U = lambda u: np.array([u ** i for i in range(3, -1, -1)])
    W = lambda w: U(w).reshape(-1, 1)

    patch = lambda u,w: np.array([
        U(u) @ basis @ control_x @ basis @ W(w),
        U(u) @ basis @ control_y @ basis @ W(w),
        U(u) @ basis @ control_z @ basis @ W(w)])

    # print(U(0.5))
    # print(W(0.5))
    # print(U(1) @ basis @ control_x @ basis @ W(1))
    # print(U(0) @ basis @ control_x @ basis @ W(0))
    # print(U(0.5) @ basis @ control_x @ basis @ W(0.5))
    # print(patch(0.5, 0.5))
    # print(patch(0, 0))
    # print(patch(1, 1))

    r = np.linspace(0,1,sample_density).reshape(-1, 1)
    s = np.linspace(0,1,sample_density).reshape(-1, 1)
    #
    # print(r.shape)
    # print(s.shape)
    #
    # print(U(r))
    # print(U(r).shape)
    print('[:,None]')
    print(U(r[:,None]).shape)
    print('[None,:]')
    print(U(r[None,:]).shape)

    # print(patch(r,s))
    # return U