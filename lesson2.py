"""
    Nonlinear convection
        \frac{ \partial u}{ \partial t} + u \frac{ \partial u }{ \partial x } = 0
        here u is the solution instead of a constant c 
    In step 1 using forward difference in time and backward difference in space
    hence,
        \frac{ u_{i}^{n+1} - u_{i}^{n} }{ \Delta t} + u_{i}^{n} \frac{ u_{i}^{n} - u_{i-1}^{n} }{ \Delta x} = 0
    

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
        u[i] = un[i] - un[i] * dt / dx * ( un[i] - un[i-1])
        
print(u)
