#!/usr/bin/env python
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('realizations',type=int, default =1,
                    help='how many cores generated independent ising sample gens')
args = parser.parse_args()
realizations = args.realizations

#inspects the data in an npz file and returns the size of the matricies and the number of samples per run
def inspect_npz(filename='samples_rank',num_npz=1):
    #look at data to determine how big to make the array scaffold
    ref = np.load(str(filename) + str(0) + '.npz')
    I = int(np.sqrt(np.size(ref[ref.files[0]])))
    N = int(len(ref))
    D = num_npz
    return I,N,D

#This loads the npz of ising models and changes them from 1/-1 to 1/0
def get_npz(I,N,D,filename='samples_rank'):
    data = np.zeros((D,N,I,I))
    for d in range(D):
        i=0
        sample = np.load(str(filename) + str(d) + '.npz')
        for sname in sample.files:
            data[d,i] = sample[sname]
            i+=1
    data = (data+1)/2
    return data

# This function sums over iterations of a run to give an average pixel value for each site in each sample
def average_pixel(data,D):
    return np.sum(data,axis=0)/D

#This finds the variance for each pixel
def var(mean,data,N,D):
    data_dummy = np.copy(data)
    for n in range(N):
        data_dummy[:,n]=(data_dummy[:,n]-mean[n])**2
    data_var_1 = np.delete(data_dummy,[N-1],axis=1)
    data_var_2 = np.delete(data_dummy,[0],axis=1)
    var_1 = np.sum(data_var_1,axis=0)/D
    var_2 = np.sum(data_var_2,axis=0)/D
    return var_1, var_2


#This finds the covariance
def covar(data,mean,N,D):
    data_dummy = np.copy(data)
    for n in range(N-1):
        data_dummy[:,n]=(data_dummy[:,n]-mean[n])*(data_dummy[:,n+1]-mean[n+1])
    data_dummy = np.delete(data_dummy,[N-1],axis=1)
    covar = np.sum(data_dummy,axis=0)/D
    return covar

#This is a function to calculata the correlation
def corr(covar,var_1,var_2,N,I):
    eta = 1*10**-10
    var_1 = var_1 + eta
    var_2 = var_2 + eta
    corr = covar/np.sqrt(var_1*var_2)
    corr = (np.sum(np.sum(np.sum(corr,axis=0),axis=0),axis=0))/((N-1)*I*I)
    return corr


I,N,D = inspect_npz(num_npz=realizations)
data = get_npz(I,N,D)
mean = average_pixel(data,D)
var_1, var_2 = var(mean,data,N,D)
cov = covar(data,mean,N,D)
cor = corr(cov,var_1,var_2,N,I)

print(cor)


