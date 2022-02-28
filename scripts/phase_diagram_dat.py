import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

#variance 
var = np.zeros((len(mag),len(temp)))

#covariance for the fit to our non_linear function (in this case a sin wave)
cov = np.zeros((len(mag),len(temp)))

#stack instances of time steps in a cycle for the length of the data collection and then caclculate the variance
how_cyclic = np.zeros((len(mag),len(temp)))
omega = 2 * np.pi / C

#fucntion for the non-linear fit
def func(t,A,phi):
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
i = 0
for t in temp:
    for m in mag:
        #load data
        data = np.genfromtxt("T"+str(t)+"_H"+str(m)+".dat",dtype=float)
        #set time and magnitization for loaded data
        time = data[:,0]
        mags = data[:,3]
        mag_squared = data[:,4]
        #var
        var[int(m*10),int(t*10)] = sum(mag_squared)/len(mag_squared)-(sum(mags**2)/len(mags))
        #save average magnetization for the loaded data
        avg_mag[int(m*10),int(t*10)] = np.mean(mags)
        #save average absolute value of the magnetization for the loaded data
        avg_abs_mag[int(m*10),int(t*10)] = np.mean(np.abs(mags))
        #use scipy function to perform the non-linear fit
        # popt, pcov = curve_fit(func, time, mags, p0=[1.0,0.1])
        #save covariance for loaded data
        # cov[int(m*10),int(t*10)]=np.sum(pcov)
        #save the cycliclicity of the loaded data
        # how_cyclic[int(m*10),int(t*10)]=cycliclicity(C,mags)
        print("site classified %s/1680" % i)
        i+=1

A = abs(avg_mag)
B = avg_abs_mag
abs_avg_mag = A

np.savetxt("abs_avg_mag.dat", abs_avg_mag)
np.savetxt("avg_abs_mag.dat", avg_abs_mag)
np.savetxt("var.dat", var)
# np.savetxt("cov.dat", cov)
# np.savetxt("how_cyclic.dat", how_cyclic)
