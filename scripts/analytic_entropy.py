import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

def onsager_entropy(tmin,tmax,J=1,T_take=0):
    Ts_fine = np.linspace(tmin, tmax, 1000)
    k = np.array((1.0 / np.sinh(2.0 / Ts_fine)) ** 2)

    def f(theta):
        return 1.0 / np.sqrt(1 - 4 * k / ((1.0 + k) ** 2) * (np.sin(theta) ** 2))
   
    def g(theta): 
        h = np.cosh(2*J/Ts_fine)**2
        return np.log(h + (1 / k) * (1 + k**2 - 2 * k * np.cos(2 * theta))**(1/2))

    Yi = integrate.quad_vec(g,0.0,(np.pi))[0]
    Xi = integrate.quad_vec(f, 0.0, np.pi / 2.0)[0]
    U_analytical = -J / np.tanh(2.0*J / Ts_fine) * (1 + 2.0 / np.pi * (2 * (np.tanh(2.0*J / Ts_fine) ** 2) - 1.0) * Xi)
    M_analytical = np.power(np.maximum(0.0, 1 - 1.0 / np.sinh(2.0 / Ts_fine) ** 4), 1.0 / 8.0)
    
    F_analytical = -Ts_fine * (np.log(2) / 2 + 1 / (2 * np.pi) * Yi)
    S = (U_analytical - F_analytical) / Ts_fine
    
    if T_take != 0:
        k = np.array((1.0 / np.sinh(2.0 / T_take)) ** 2)

        def f(theta):
            return 1.0 / np.sqrt(1 - 4 * k / ((1.0 + k) ** 2) * (np.sin(theta) ** 2))
   
        def g(theta): 
            h = np.cosh(2*J/T_take)**2
            return np.log(h + (1 / k) * (1 + k**2 - 2 * k * np.cos(2 * theta))**(1/2))

        Yi = integrate.quad_vec(g,0.0,(np.pi))[0]
        Xi = integrate.quad_vec(f, 0.0, np.pi / 2.0)[0]
        U_take = -J / np.tanh(2.0*J / T_take) * (1 + 2.0 / np.pi * (2 * (np.tanh(2.0*J / T_take) ** 2) - 1.0) * Xi)
        M_take = np.power(np.maximum(0.0, 1 - 1.0 / np.sinh(2.0 / T_take) ** 4), 1.0 / 8.0)
        
        F_take = -T_take * (np.log(2) / 2 + 1 / (2 * np.pi) * Yi)
        S_take = (U_take - F_take) / T_take


    # Set up plot
    # fig, ax = plt.subplots(3, 1, sharex=True)
    #
    # ax[0].plot(Ts_fine, U_analytical, linewidth=2.0, label="Analytical")
    # ax[1].plot(Ts_fine, M_analytical, linewidth=2.0)
    # ax[2].plot(Ts_fine, S, linewidth=2.0)
    #
    # Plot formatting
    # ax[1].set_xlabel('T')
    # ax[1].set_ylabel(r'$\mathrm{\left|m\right|}$')
    # ax[0].set_xlabel('T')
    # ax[0].set_ylabel('E')
    # ax[2].set_xlabel('T')
    # ax[2].set_ylabel('S')
    # ax[0].legend()
    # plt.subplots_adjust(hspace=0.0)
    #
    # plt.show()
    return S_take
