#!/usr/bin/env python
from sys import argv
import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
import numpy as np
from dataset_prep import like_mnist
import pickle
import os
import argparse
import configparser
from item_name import item_name
from ising_models_secondary_keys_non_equ import secondary_keys

config = configparser.ConfigParser()
config.read("run.param")
T = float(config['input']['T'])
L = int(config['input']['L'])
epochs = int(config['input']['epochs'])
batch_size = int(config['input']['batch_size']) 
learning_rate = float(config['input']['learning_rate']) 
shuffbuff = int(config['input']['shuffbuff']) 
training_samples = int(config['input']['training_samples']) 
test_samples = int(config['input']['test_samples']) 
heirarchies = int(config['input']['heirarchies']) 
filters = int(config['input']['filters']) 
logistic_mix = int(config['input']['logistic_mix']) 
dropout = float(config['input']['dropout']) 
# n_samples = int(config['input']['n_samples'])
p = dict(config['input'])

tfd = tfp.distributions
tfk = tf.keras
tfkl = tf.keras.layers

#n_samples temp definition
n_samples=4

#load samples to attempt avoiding need to generate samples
shape, data = like_mnist(T,L)
data = data.shuffle(shuffbuff)

results = []

image_shape = (L,L,1)

# Define a Pixel CNN network
dist = tfd.PixelCNN(
    image_shape=image_shape,
    num_resnet=1,
    num_hierarchies=3,
    num_filters=32,
    num_logistic_mix=5,
    dropout_p=.3,
    high=1
)

# Define the model input
image_input = tfkl.Input(shape=image_shape)

# Define the log likelihood for the loss fn
log_prob = dist.log_prob(image_input)

# Define the model
model = tfk.Model(inputs=image_input, outputs=log_prob)
model.add_loss(-tf.reduce_mean(log_prob))
p['T']=T
del p['t']
del p['n_samples']

secondary_keys.remove('n_samples')
model_dir = item_name("/gcohenlab/data/samuelgelman/data/ising_models/final_models",p,secondary_keys)

model.load_weights(str(model_dir)+"/weights_"+str(epochs)+"/cp.ckpt")

# sample n images from the trained model
print("Sampling...")
samples = dist.sample(n_samples)

np.savez('sample.npz',samples)
