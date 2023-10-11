# Step 7: 2D Diffusion

"""
    2D Diffusion Equation:
        \partial u / \partial t = \nu \partial^2 u / \partial x^2  + \nu \partial^2 u / \partial y^2
        
    Discretization: 
        + Timestep: Forward difference
        + Spatial steps: Two second order derivatives
        (u[i, j] - un[i,j]) / dt = nu (un[i+1, j] - 2 un[i, j] + un[i-1, j] ) / dx^2 + nu (un[i, j+1] - 2 un[i, j] + un[i, j-1] ) / dy^2
        
    Solve for unknonw:
        u[i, j] = un[i, j] + nu dt /dx^2 (un[i+1, j] - 2 un[i, j] + un[i-1, j] )
                           + nu dt /dy^2 (un[i, j+1] - 2 un[i, j] + un[i, j-1] )
        
"""

import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D

# Vairable declarations
nx = 31
ny = 31
nt = 17
nu = .05
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = .25
dt = sigma * dx * dy / nu

x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((ny, nx))
un = numpy.ones((ny, nx))




def diffuse(nt):
    # Initial conditions
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
    
    for n in range(nt+1):
        un = u.copy()
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] +
                         nu * dt / dx**2 *
                         (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                         nu * dt / dy**2 *
                         (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]))
        u[0, :] = 1
        u[-1, : ] = 1
        u[:, 0] = 1
        u[:, -1] = 1
    # fig = pyplot.figure()
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(X, Y, u[:], rstride=1, cstride=1, cmap=cm.viridis,
    #     linewidth=0, antialiased=True)
    # ax.set_zlim(1, 2.5)
    # ax.set_xlabel('$x$')
    # ax.set_ylabel('$y$');
        
diffuse(10)        
