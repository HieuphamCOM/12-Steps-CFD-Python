# Step 1: 1D Linear Convection
"""
    1D Linear convection: \frac{ \partial{u} }{ \partial{t} } + c \frac{ \partial{u} }{ \partial{x} } = 0
    Initial condition (~ a wave)
    speed c represents the propagation of the intial wave, without change of shape
    u(x, 0) = u_0(x)
    Exact: u(x, t) = u_0(x - ct)
"""

"""
    Discrete equation:
    \frac{ u_{i}^{n+1} - u_{i}^{n} }{ \Delta t } + c \frac{ u_{i}^{n} - u_{i-1}^{n} }{ \Delta x } = 0
    <=>
    u_{i}^{n+1} = u_{i}^{n} - c \frac{ \Delta t }{ \Delta x } ( u_{i}^{n} - u_{i-1}^{n} )
"""

import numpy                    # useful matrix operations
from matplotlib import pyplot   # 2D plotting library
import time, sys                # used to slow down animations for viewing

nx = 41
dx = 2 / (nx-1)
nt = 25
dt = .025
c = 1

# initialization
u = numpy.ones(nx)
u[int(.5 / dx) : int(1 / dx  + 1)] = 2
print(u)

un = numpy.ones(nx)

for n in range(nt):
    un = u.copy() #copy existing values of u into un
    for i in range(1, nx): 
        u[i] = un[i] - c * dt / dx * ( un[i] - un[i-1])
        
print(u)
