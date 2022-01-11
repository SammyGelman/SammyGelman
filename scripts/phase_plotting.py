import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# fig, ax = subplots(2, 2)
# ax[0][0].imshow((1-A) * B)
# ax[1][0].imshow(norm_icov)
# ax[1][1].imshow(norm_how_cyclic)

A = np.genfromtxt("abs_avg_mag.dat",dtype=float)

B = np.genfromtxt("avg_abs_mag.dat",dtype=float)

# cov = np.genfromtxt("cov.dat",dtype=float)

# how_variant = np.genfromtxt("how_cyclic.dat",dtype=float)
# how_variant = how_variant/np.max(how_variant)
var = abs(np.genfromtxt("var.dat",dtype=float))

# C1 = np.array([0.0, 0.1, 0.0] * 41 * 41).reshape(41, 41, 3)
C1 = 1.0*np.array([0.16, 0.56, 0.75] * 41 * 41).reshape(41, 41, 3)
C2 = 1.0*np.array([0.25, 0.75, 0.30] * 41 * 41).reshape(41, 41, 3)
# C3 = 0.0*np.array([0.26, 0.30, 0.53] * 41 * 41).reshape(41, 41, 3)
C4 = 1.0*np.array([.922, 0.11, 0.158] * 41 * 41).reshape(41, 41, 3)

# imAB = np.einsum('ij,ijk->ijk', A * B, C1)
imAB = np.einsum('ij,ijk->ijk', A, C1)
im1mAB = np.einsum('ij,ijk->ijk', (1-A) * B, C2)
# imnorm_icov = np.einsum('ij,ijk->ijk', norm_icov, C3)
# imnorm_icov = np.einsum('ij,ijk->ijk', cov , C3)
# imnorm_how_cyclic = np.einsum('ij,ijk->ijk', norm_how_cyclic, C4)
imvar = np.einsum('ij,ijk->ijk', var, C4)
# imvar = np.einsum('ij,ijk->ijk', var, C4)

axis = [0.0 , 4.0, 0.0 , 4.0]

# plt.imshow((imAB + im1mAB + imnorm_icov + imnorm_how_cyclic)[::-1,:,:],extent=axis)
plt.imshow((imAB + im1mAB + imvar)[::-1,:,:],extent=axis)
# plt.imshow(imAB + im1mAB + imnorm_icov + imnorm_how_cyclic, interpolation='nearest')
plt.ylabel('Magnetic Field Strength')
plt.xlabel('Temperature')
plt.title('Phase Diagram for Ising Model with Oscillating Magnetic Field')
plt.show()
