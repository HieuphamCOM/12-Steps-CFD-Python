# Step 3: Convergence and the CFL condition
"""

"""

import numpy                    # useful matrix operations
from matplotlib import pyplot   # 2D plotting library
import time, sys                # used to slow down animations for viewing

def linearconv(nx):
    dx = 2 / (nx-1)
    nt = 20
    c = 1
    sigma = .5
    
    dt = sigma * dx

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

nx = 41
linearconv(nx)