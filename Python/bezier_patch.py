def bezier_patch(control_x, control_y, control_z, sample_density):
    import numpy as np
    basis = [[-1,  3, -3, 1],
             [ 3, -6,  3, 0],
             [-3,  3,  0, 0],
             [ 1,  0,  0, 0]]
    basis = np.array(basis)
    U = lambda u: [u ** i for i in range(3, -1, -1)]
    print(U(3))
    # return U