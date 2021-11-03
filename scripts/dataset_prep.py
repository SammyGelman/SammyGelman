#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import pickle
import random

def like_mnist(T,L,sample_batches=27,buffer_size=1):

    def sample_prep(sample):
        sample = np.array(sample)
        sample = np.where(sample==-1,0,sample)
        sample = sample[..., np.newaxis]
        sample_dict = {'image': sample, 'label': ()}
        return sample_dict

    def get_samples(filename):
        samples = np.load(filename)
        for sname in samples.files:
            yield sample_prep(samples[sname])

    shape = (int(L),int(L),1)
    ds_samples = tf.data.Dataset.from_generator(
        get_samples,
        # args=['/gcohenlab/data/samuelgelman/data/ising_data/ising_samples_l'+str(L)+'/T'+str(T)+'/samples_rank'+str(int(batch))+'.npz'],
        args=['/gcohenlab/data/samuelgelman/data/ising_data/ising_samples_l'+str(L)+'/T'+str(T)+'/final_samples.npz'],
        output_types={'image': tf.int64, 'label': tf.float64},
        output_shapes={'image': shape, 'label': None}
        )
    ds_samples = tf.data.Dataset.prefetch(ds_samples,buffer_size)
    return shape, ds_samples
