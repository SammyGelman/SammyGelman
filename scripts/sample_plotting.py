#!/usr/bin/env python
import sys
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
from ising_models_secondary_keys import secondary_keys

# parser = argparse.ArgumentParser()
# parser.add_argument('checkpoints',type=str, default='weights',
#                     help='this is a path to the directory containing the pretrained weights')
# parser.add_argument('samples',type=int, default =9,
#                     help='these are the epochs')
# parser.add_argument('length',type=int, default =8,
#                     help='length of lattice')
# args = parser.parse_args()

# T = args.temprature[0]
# l = args.length
# n = args.samples
# cp_path = args.checkpoints

config = configparser.ConfigParser()
config.read("run.param")
T = float(config['input']['T'])
l = int(config['input']['L'])
epochs = int(config['input']['epochs'])
# n = int(config['input']['n_samples'])
n=5
p = dict(config['input'])

tfd = tfp.distributions
tfk = tf.keras
tfkl = tf.keras.layers

# tf.enable_v2_behavior()
results = []

def image_preprocess(x):
    x['image'] = tf.cast(x['image'], tf.float32)
    return (x['image'],)  # (input, output) of the model

# train_it = train_data.map(image_preprocess).batch(batch_size).shuffle(1000)

# image_shape = shape
image_shape = (l,l,1)
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

# Load pre-existing ones
model_dir = item_name("/media/sammy/scratch/data/ising_models/model_weights",p,secondary_keys)

model.load_weights(str(model_dir)+"/weights/cp.ckpt")

# sample n images from the trained model
print("Sampling...")
samples = dist.sample(n)

# Plot samples:
entropies = []
print("Plotting...")
import matplotlib.pyplot as plt
for sample in samples:
    entropies.append(dist.log_prob(sample).numpy())
    s = sample.numpy()[:,:,0]
    plt.matshow(s)
plt.show()
