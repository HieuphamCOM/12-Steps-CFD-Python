# Step 4: Burger's Equation
"""
    Burger's equation in 1D:
        \frac{ \partial u}{ \partial t} + u \frac{ \partial u }{ \partial x } = \nu \frac{ \partial^2 u }{ \partial x^2 }
    A burger's equation contains :
        + non-linear convection term: u \frac{ \partial u }{ \partial x } 
        + diffusion term: \nu \frac{ \partial^2 u }{ \partial x^2 }
    Methodology: 
        + using forward difference for time
        + backward difference for space
        + 2nd order method for the second derivatives
    
    Hence:
        u_{i}^{n+1} = u_{i}^{n} - u_{i}^{n} \frac{ \Delta t }{ \Delta x } ( u_{i}^{n} - u_{i-1}^{n} ) + \nu \frac{ \Delta t}{ \Delta x^2 } ( u_{i+1}^{n} - 2 u_{i}^{n} + u_{i-1}^{n} )
    
    
    For a Burger's equation, we use two different IC and BC
        First:
            + u = - \frac{ 2 \nu}{ \phi } \frac{ \partial phi }{ \partial x } + 4
            + \phi = exp( \frac{ - x^2 }{ 4 \nu }) + exp( \frac{ - ( x - 2 \pi )^2}{ 4 \nu } )
        Second:
            + u = - \frac{ 2 \nu}{ \phi } \frac{ \partial phi }{ \partial x } + 4
            + \phi = exp( \frac{ - ( x - 4 t)^2 }{ 4 \nu ( t  + 1 )}) + exp( \frac{ - ( x - 4t - 2 \pi )^2}{ 4 \nu (t + 1) } )
            
    BC: 
        + u(0) = u(2 \pi)
    
"""

import numpy
import sympy

from sympy import init_printing
from sympy.utilities.lambdify import lambdify
from matplotlib import pyplot

init_printing(use_latex=True)

x, nu, t = sympy.symbols('x nu t')
phi = ( sympy.exp( - (x - 4 * t)**2 / (4 * nu * (t+1)))) +  sympy.exp( - (x - 4 * t - 2 * sympy.pi )**2 / (4 * nu * (t+1)))

phiprime = phi.diff(x)
print(phiprime)

u = -2 * nu * ( phiprime / phi) + 4
print(u)

# Lambdify
ufunc = lambdify((t, x, nu), u)
print(ufunc(1, 4, 3))

# Burger's equation
nx = 101
nt = 100
dx = 2 * numpy.pi / (nx-1)
nu = .07
dt = dx * nu

x = numpy.linspace(0, 2 * numpy.pi, nx)
un = numpy.empty(nx)
t = 0

u = numpy.asarray([ufunc(t, x0, nu) for x0 in x]) # here is the initialcondition
print(u)

# Peridodic BC
for n in range(nt):
    un = u.copy()
    for i in range(1, nx - 1):
        u[i] = un[i] - un[i] * dt / dx * ( un[i] - un[i-1] ) + nu * dt / dx**2 *\
            ( un[i+1] - 2 * un[i] + un[i-1])
        u[0] = un[0] - un[0] * dt / dx * ( un[0] - un[-2] ) + nu * dt / dx**2 *\
            ( un[1] - 2 * un[0] + un[-2])
        u[-1] = u[0]
u_analytical = numpy.asarray([ufunc(nt * dt, xi, nu) for xi in x])