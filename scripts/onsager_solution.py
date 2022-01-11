import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def onsager_entropy(t,J=1):
    k = np.array((1.0 / np.sinh(2.0 / t)) ** 2)

    def f(theta):
        return 1.0 / np.sqrt(1 - 4 * k / ((1.0 + k) ** 2) * (np.sin(theta) ** 2))
   
    def g(theta): 
        h = np.cosh(2*J/t)**2
        return np.log(h + (1 / k) * (1 + k**2 - 2 * k * np.cos(2 * theta))**(1/2))

    Yi = integrate.quad_vec(g,0.0,(np.pi))[0]
    Xi = integrate.quad_vec(f, 0.0, np.pi / 2.0)[0]
    U_analytical = -J / np.tanh(2.0*J / t) * (1 + 2.0 / np.pi * (2 * (np.tanh(2.0*J / t) ** 2) - 1.0) * Xi)
    M_analytical = np.power(np.maximum(0.0, 1 - 1.0 / np.sinh(2.0 / t) ** 4), 1.0 / 8.0)
    
    F_analytical = -t * (np.log(2) / 2 + 1 / (2 * np.pi) * Yi)
    S = (U_analytical - F_analytical) / t
    
    return S
