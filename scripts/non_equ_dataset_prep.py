#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import pickle
import random
from item_name import item_name
import configparser
from non_equ_secondary_keys import secondary_keys

# config = configparser.ConfigParser()
# config.optionxform = str
# config.read("run.param")
# T = float(config['input']['T'])
# L = int(config['input']['L'])
# H = float(config['input']['H'])
# J = float(config['input']['J'])
# C = float(config['input']['C'])
# epochs = int(config['input']['epochs'])
# batch_size = int(config['input']['batch_size'])
# learning_rate = float(config['input']['learning_rate'])
# shuffbuff = int(config['input']['shuffbuff'])
# training_samples = int(config['input']['training_samples'])
# test_samples = int(config['input']['test_samples'])
# heirarchies = int(config['input']['heirarchies'])
# filters = int(config['input']['filters'])
# logistic_mix = int(config['input']['logistic_mix'])
# dropout = float(config['input']['dropout'])
# n_samples = int(config['input']['n_samples'])
# p = dict(config['input'])
#
# print(p)
# p['T']=T
# del p['t']
#
def like_mnist(prefix,t,T,L,H,sample_batches=27,buffer_size=1):
# def like_mnist(prefix,T,L,H,sample_batches=27,buffer_size=1):
    # path ='/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/t'+str(t)+'_samples.npz'
    # path ='/gcohenlab/data/samuelgelman/data/non_equ_data/'+str(prefix)+'_H'+str(H)+'/slice_'+str(t)+'.npz'
    # path ='/home/sammy/gcohenlabfs/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/t'+str(t)+'_samples.npz'

    # raw_data = np.load(path)['arr_0']

    def sample_prep(sample):
        sample = np.array(sample)
        sample = np.where(sample==-1,0,sample)
        sample = sample[..., np.newaxis]
        sample_dict = {'image': sample, 'label': ()}
        return sample_dict

    # def data_gen(data):
    #     i=0
    #     while i < len(data):
    #         yield sample_prep(data[i])
    #         i+=1
    
    def get_samples(filename):
        samples = np.load(filename)
        for sname in samples.files:
            yield sample_prep(samples[sname])

    shape = (int(L),int(L),1)
    sample_batches_rand = np.linspace(0,sample_batches-1,sample_batches)
    random.shuffle(sample_batches_rand)
    for batch in sample_batches_rand:
        # path ='/gcohenlab/data/samuelgelman/data/non_equ_data/phase_diagram_data/'+str(prefix)+'_T'+str(T)+"/samples_rank"+str(int(batch))+'.npz'
        # model_dir = item_name("/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples",p,secondary_keys, excluded_keys=['n_samples'])
        # model_dir = item_name("/gcohenlab/data/samuelgelman/data/non_equ_data/linear_response_H1.0/slice_"+str(t)+".npz")
        ds_samples = tf.data.Dataset.from_generator(
            # data_gen,
            get_samples,
            # args=[raw_data],
            # args=[path],
            #args=['/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/t'+str(t)+'_samples.npz'],
            args=["/gcohenlab/data/samuelgelman/data/non_equ_data/linear_response_H1.0/slice_"+str(t)+".npz"],
            output_types={'image': tf.int64, 'label': tf.float64},
            output_shapes={'image': shape, 'label': None}
        )
        ds_samples = tf.data.Dataset.prefetch(ds_samples,buffer_size)
    return shape, ds_samples
