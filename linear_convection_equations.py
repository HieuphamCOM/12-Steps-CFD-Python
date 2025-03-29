# Step 7: 2D Linear convection
"""
    In 2D:
        x_i = x_0 + i \Delta x
        y_i = y_0 + i \Delta y
        u_{i, j} = u(x_i, y_j)
        
    First-order partial derivative in x-di, finite-difference formula:
        (\partial u / \partial x)at i, j = u[i+1, j] - u[i, j] / \Delta x + O(\Delta x)
        in y-di
        (\partial u / \partial y)at i, j = u[i, j+1] - u[i, j] / \Delta y + O(\Delta x)
        
    PDE governing 2-D Linear convection is:
        \partial u / \partial t + c \partial u / \partial x + c \partial u / \partial y = 0
        
    Discretization:
        + Timestep : forward difference
        + Spatial steps: backward differences
        ( u[i, j] - un[i, j] ) / dt + c ( un[i, j] - un[i-1, j] ) / dx + c ( un[i, j] - un[i, j-1] ) / dy = 0
        <=>
        u[i, j] = un[i, j] - c dt / dx ( un[i, j] - un[i-1, j] ) - c dt / dy ( un[i, j] - un[i, j-1] ) 
        
    Given initial conditions:
        u(x ,y) = 2 for 0.5 <= x, y <= 1
                  1 for else
    
    Boundary conditions
        u = 1 for x = 0 , 2
                  y = 0 , 2
"""

from mpl_toolkits.mplot3d import Axes3D # Library used for projected 3d plots

import numpy
from matplotlib import pyplot, _cm

# variable declarations
nx = 81
ny = 81
nt = 100
c = 1
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = .2
dt = sigma * dx

x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((ny, nx))
un = numpy.ones((ny, nx))

# Initial condition
u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 

# Iterating in two dimensions
for n in range(nt + 1):
    un = u.copy()
    u[1:, 1:] = ( un[ 1:, 1: ] - ( c * dt / dx * ( un[ 1: , 1: ] - un[ 1: , 0:-1 ] ) )
                               - ( c * dt / dy * ( un[ 1: , 1: ] - un[ 0:-1 , 1: ] ) ) )
    u[0, :] = 1
    u[-1, : ] = 1
    u[:, 0] = 1
    u[:, -1] = 1
