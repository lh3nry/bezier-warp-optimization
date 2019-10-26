import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

R = 1.
r = 0.8
n = 50
m = 50

def torus_triangles(n, m):
    """ Returns triangles to mesh a (n, m) torus """
    tri = []
    for i in range(n):
        for j in range(m):
            a = i + j*(n)
            b = ((i+1) % n) + j*n
            d = i + ((j+1) % m) * n
            c = ((i+1) % n) + ((j+1) % m) * n
            tri += [[a, b, d], [b, c, d]]
    return np.array(tri, dtype=np.int32)

theta0 = np.linspace(0, (2*np.pi), n, endpoint=False)
phi0 = np.linspace(0, (2*np.pi), m, endpoint=False)
theta, phi = np.meshgrid(theta0, phi0)

x = (R + r * np.sin(phi)) * np.cos(theta)
y = (R + r * np.sin(phi)) * np.sin(theta)
z = r * np.cos(phi)

triangles = torus_triangles(n , m)
triang = mtri.Triangulation(x.ravel(), y.ravel(), triangles)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(triang, z.ravel(), lw=0.2, edgecolor="black", color="grey",
                alpha=0.5)

plt.show()

