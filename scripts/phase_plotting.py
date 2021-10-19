import numpy as np
import matplotlib.pyplot as plt

# fig, ax = subplots(2, 2)
# ax[0][0].imshow((1-A) * B)
# ax[1][0].imshow(norm_icov)
# ax[1][1].imshow(norm_how_cyclic)

#set range which matches available data, apologies for the hard coding
mag = np.around(np.linspace(0.0,4.0,41),decimals=1)
temp = np.around(np.linspace(0.0,4.0,41),decimals=1)

#Cycle length
C = 50

#Create empty arrays for the classification of model behaviour at given parameters

#average magnetization 
avg_mag = np.zeros((len(mag),len(temp)))
#average of the absolute value of the magnetization
avg_abs_mag = np.zeros((len(mag),len(temp)))
#covariance for the fit to our non_linear function (in this case a sin wave)
cov = np.zeros((len(mag),len(temp)))
#stack instances of time steps in a cycle for the length of the data collection and then caclculate the variance
how_cyclic = np.zeros((len(mag),len(temp)))

#fucntion for the non-linear fit
def func(t,A,omega,phi):
    return A*np.sin(t*omega+phi)

#measures how much vairance there is between cycles
def cycliclicity(C,m):
     slices = [ [] for _ in range(C) ]
     slice_var = np.zeros((C))
     for i in range(len(m)):
         slices[i%C].append(m[i])
     for i in range(C):
         slice_var[i]=np.var(slices[i])
     return sum(slice_var)

#The loop which goes through all availbale data collects metrics which will be used for classification
for m in mag:
    for t in temp:
        #load data
        data = np.genfromtxt("mag_"+str(m)+"_temp_"+str(t)+".dat",dtype=float)
        #set time and magnitization for loaded data
        time = data[:,0]
        mags = data[:,3]
        #save average magnetization for the loaded data
        avg_mag[int(m*10),int(t*10)] = np.mean(mags)
        #save average absolute value of the magnetization for the loaded data
        avg_abs_mag[int(m*10),int(t*10)] = np.mean(np.abs(mags))
        #use scipy function to perform the non-linear fit
        popt, pcov = curve_fit(func, time, mags,p0=[1,(2*np.pi/50),0])
        #save covariance for loaded data
        cov[int(m*10),int(t*10)]=np.sum(pcov)
        #save the cycliclicity of the loaded data
        how_cyclic[int(m*10),int(t*10)]=cycliclicity(C,mags)
 
A = abs(avg_mag)
B = avg_abs_mag

C1 = np.array([1.0, 0.8, 0.0] * 41 * 41).reshape(41, 41, 3)
C2 = np.array([0.0, 0.5, 1.0] * 41 * 41).reshape(41, 41, 3)
C3 = np.array([0.0, 1.0, 0.0] * 41 * 41).reshape(41, 41, 3)
C4 = np.array([1.0, 0.0, 0.0] * 41 * 41).reshape(41, 41, 3)

AB = np.einsum('ij,ijk->ijk', A * B, C1)
m1mAB = np.einsum('ij,ijk->ijk', (1-A) * B, C2)
imnorm_icov = np.einsum('ij,ijk->ijk', norm_icov, C3)
imnorm_how_cyclic = np.einsum('ij,ijk->ijk', norm_how_cyclic, C4)

imshow(imAB + im1mAB + imnorm_icov + imnorm_how_cyclic)
ylabel('Magnetic Field Strength')
xlabel('Temperature')
title('Phase Diagram for Ising Model with Oscillating Magnetic Field')

