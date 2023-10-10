# Step 3: Diffusion equation in 1D
"""
    1D diffusion equation:
        \frac{ \partial u }{ \partial t } = \nu \frac{ \partial^2 u }{ \partial x^2}
        Note: this one has a 2nd order derivative
    Discretize the 2nd order derivative with a Central Difference scheme
        + Forward Difference 
        + Backward Diference 
    Consider the Taylor expansion of u_{i+1} and u_{i-1} around u_{i}
        + u_{i+1} &= u_{i} + \Delta x \frac{ \partial u }{ \partial x } + \frac{ \Delta x^2 }{ 2 } \frac{ \partial^2 u }{ \partial x^2} at i \\
                    + \frac{ \Delta x^3 }{ 3! } \frac{ \partial^3 u }{ \partial x^3} at i + \mathcal{O} (\Delta x^4) 
        + u_{i-1} &= u_{i} - \Delta x \frac{ \partial u }{ \partial x } + \frac{ \Delta x^2 }{ 2 } \frac{ \partial^2 u }{ \partial x^2} at i \\
                    - \frac{ \Delta x^3 }{ 3! } \frac{ \partial^3 u }{ \partial x^3} at i + \mathcal{O} (\Delta x^4) 
    Hence, 
        u_{i+1} + u_{i-1} = 2 u_{i} + \Delta x^2 \frac{ \partial^2 u }{ \partial x^2 } at i + \mathcal{O} (\Delta x^4)
    Therefore, 
        \frac{ \partial^2 u}{\partial x^2} = \frac{ u_{i+1} - 2 u_{i} + u_{i-1} }{ \Delta x^2 } + \mathcal{O} ( \Delta x^2 )
        
    1D diffusion equation can be written as:    
        u_{i}^{n+1} = u_{i}^{n} + \frac{ \nu \Delta t}{ \Delta x^2 } (u_{i+1}^{n} - 2 u_{i}^{n} + u_{i-1}^{n})

"""

import numpy                    # useful matrix operations
from matplotlib import pyplot   # 2D plotting library
import time, sys                # used to slow down animations for viewing

def linearconv(nx):
    dx = 2 / (nx-1)
    nt = 20
    c = 1
    nu = .3
    sigma = .2
    
    dt = sigma * dx**2 / nu

    # initialization
    u = numpy.ones(nx)
    u[int(.5 / dx) : int(1 / dx  + 1)] = 2

    un = numpy.ones(nx)

    for n in range(nt):
        un = u.copy() #copy existing values of u into un
        for i in range(1, nx - 1): 
            u[i] = un[i] + nu * dt / dx**2 * ( un[i+1] - 2 * un[i] + un[i+1])
            
    print(u)

nx = 41
linearconv(nx)
