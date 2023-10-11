# Step 8: Burger's Equation in 2D

"""
    Burger's equation possibly generates discontinuous solutions from a smooth initial condition
    
    PDEs:
        \partial u / \partial t + u \partial u / \partial x + v \partial u / \partial y = nu ( \partial^2 u / partial x^2 + \partial^2 u / \partial y^2)
        \partial v / \partial t + u \partial v / \partial x + v \partial v / \partial y = nu ( \partial^2 v / partial x^2 + \partial^2 v / \partial y^2)
        
    Discretization: 
        + Timestep: Forward difference
        + Spatial steps: Two second order derivatives
        (u[i, j] - un[i, j]) / dt + un[i, j] (un[i, j] - un[i-1, y]) / dx + vn[i, j] (un[i, j] - un[i, j - 1]) / dy 
                    = nu (un[i+1, j] - 2 un[i, j] + un[i-1, j] ) / dx^2 + nu (un[i, j+1] - 2 un[i, j] + un[i, j-1] ) / dy^2
        (v[i, j] - vn[i, j]) / dt + un[i, j] (vn[i, j] - vn[i-1, y]) / dx + vn[i, j] (vn[i, j] - vn[i, j - 1]) / dy
                    = nu (vn[i+1, j] - 2 vn[i, j] + vn[i-1, j] ) / dx^2 + nu (vn[i, j+1] - 2 vn[i, j] + vn[i, j-1] ) / dy^2
                    
    Solve for unknowns:
        u[i, j] = un[i, j] - un[i, j] dt / dx (un[i, j] - un[i-1, j]) - vn[i, j] dt / dx (un[i, j] - un[i, j-1]) 
                    + nu dt /dx^2 (un[i+1, j] - 2 un[i, j] + un[i-1, j] )
                    + nu dt /dy^2 (un[i, j+1] - 2 un[i, j] + un[i, j-1] )
        v[i, j] = vn[i, j] - un[i, j] dt / dx (vn[i, j] - vn[i-1, j]) - vn[i, j] dt / dx (vn[i, j] - vn[i, j-1]) 
                    + nu dt /dx^2 (vn[i+1, j] - 2 vn[i, j] + vn[i-1, j] )
                    + nu dt /dy^2 (vn[i, j+1] - 2 vn[i, j] + vn[i, j-1] )
"""

import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D
# %matplotlib inline

# Vairable declarations
nx = 41
ny = 41
nt = 120
nu = .01
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = .0009
dt = sigma * dx * dy / nu

x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((ny, nx))
un = numpy.ones((ny, nx))
v = numpy.ones((ny, nx))
vn = numpy.ones((ny, nx))
comb = numpy.ones((ny, nx))



def burger_2d(nt):
    
    #Initial conditions
    u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
    v[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
    
    for n in range(nt+1):
        un = u.copy()
        vn = v.copy()
        
        u[1:-1, 1:-1] = ( un[1:-1, 1:-1]
                        - ( un[1:-1, 1:-1] * dt / dx * ( un[1:-1, 1:-1] - un[1:-1 , 0:-2] ) )
                        - ( vn[1:-1, 1:-1] * dt / dy * ( un[1:-1, 1:-1] - un[0:-2 , 1:-1] ) ) 
                        + nu * dt / dx**2 *
                         (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2])
                        + nu * dt / dy**2 *
                         (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1]) )
        
        v[1:-1, 1:-1] = ( vn[1:-1, 1:-1]
                        - ( un[1:-1, 1:-1] * dt / dx * ( vn[1:-1, 1:-1] - vn[1:-1 , 0:-2] ) )
                        - ( vn[1:-1, 1:-1] * dt / dy * ( vn[1:-1, 1:-1] - vn[0:-2 , 1:-1] ) ) 
                        + nu * dt / dx**2 *
                         (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2])
                        + nu * dt / dy**2 *
                         (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1]) )
        
        
        u[0, :] = 1
        u[-1, : ] = 1
        u[:, 0] = 1
        u[:, -1] = 1
        v[0, :] = 1
        v[-1, : ] = 1
        v[:, 0] = 1
        v[:, -1] = 1
        # fig = pyplot.figure(figsize=(11, 7), dpi=100)
        # ax = fig.add_subplot(projection='3d')
        # X, Y = numpy.meshgrid(x, y)
        # ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=1, cstride=1)
        # ax.plot_surface(X, Y, v, cmap=cm.viridis, rstride=1, cstride=1)
        # ax.set_xlabel('$x$')
        # ax.set_ylabel('$y$');
        
burger_2d(nt)
