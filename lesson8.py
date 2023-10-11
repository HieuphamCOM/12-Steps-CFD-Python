# Step 6: 2D Convection
"""
    2D Convection presented by the pair of coupled partial differential equations:
        \partial u / \partial t + u \partial u / \partial x + v \partial u / \partial y = 0
        \partial v / \partial t + u \partial v / \partial x + v \partial v / \partial y = 0
        
    Discretization:
        + Timestep: Forward difference
        + Spatial steps: Backward differences
        (u[i, j] - un[i, j]) / dt + un[i, j] (un[i, j] - un[i-1, y]) / dx + vn[i, j] (un[i, j] - un[i, j - 1]) / dy = 0
        (v[i, j] - vn[i, j]) / dt + un[i, j] (vn[i, j] - vn[i-1, y]) / dx + vn[i, j] (vn[i, j] - vn[i, j - 1]) / dy = 0
        
    Solve for unknowns:
        u[i, j] = un[i, j] - un[i, j] dt / dx (un[i, j] - un[i-1, j]) - vn[i, j] dt / dx (un[i, j] - un[i, j-1]) 
        v[i, j] = vn[i, j] - un[i, j] dt / dx (vn[i, j] - vn[i-1, j]) - vn[i, j] dt / dx (vn[i, j] - vn[i, j-1]) 
        
    Initial conditions:
        u, v= 2 for x, y in (0.5, 1) X (0.5, 1)
              1 for else
              
    Boundary conditions:
        u = 1, v = 1 for x = 0 , 2
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
v = numpy.ones((ny, nx))
vn = numpy.ones((ny, nx))

# Initial condition
u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
v[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 

# Iterating in two dimensions
for n in range(nt + 1):
    un = u.copy()
    vn = v.copy()
    
    
    u[1:, 1:] = ( un[ 1:, 1: ] - ( un[1:, 1:] * dt / dx * ( un[ 1: , 1: ] - un[ 1: , 0:-1 ] ) )
                               - ( vn[1:, 1:] * dt / dy * ( un[ 1: , 1: ] - un[ 0:-1 , 1: ] ) ) )
    
    v[1:, 1:] = ( vn[ 1:, 1: ] - ( un[1:, 1:] * dt / dx * ( vn[ 1: , 1: ] - vn[ 1: , 0:-1 ] ) )
                               - ( vn[1:, 1:] * dt / dy * ( vn[ 1: , 1: ] - vn[ 0:-1 , 1: ] ) ) )
    u[0, :] = 1
    u[-1, : ] = 1
    u[:, 0] = 1
    u[:, -1] = 1
    v[0, :] = 1
    v[-1, : ] = 1
    v[:, 0] = 1
    v[:, -1] = 1