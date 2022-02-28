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
import time 

# parser = argparse.ArgumentParser()
# parser.add_argument('checkpoints',type=str, default='weights',
#                     help='this is a path to the directory containing the pretrained weights')
# parser.add_argument('samples',type=int, default =9,
#                     help='these are the epochs')
# parser.add_argument('length',type=int, default =8,
#                     help='length of lattice')
# args = parser.parse_args()
#
# l = args.length
# n = args.samples
# cp_path = args.checkpoints

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
n_samples = int(config['input']['n_samples'])
p = dict(config['input'])

p['T']=T
del p['t']
del p['n_samples']

tfd = tfp.distributions
tfk = tf.keras
tfkl = tf.keras.layers

secondary_keys.remove('n_samples')

# for i in range(15):
#n_samples temp definition
n_samples=100

for i in range(15):
    #load samples to attempt avoiding need to generate samples
    shape, data = like_mnist(T,L)
    data = data.shuffle(1000)
    data = data.repeat(2)
    # data = data.shuffle(shuffbuff)
    samples_mc = data.take(n_samples)

    # tf.enable_v2_behavior()
    results = []
    image_shape = (L,L,1)

    # Define a Pixel CNN network
    dist = tfd.PixelCNN(
        image_shape=image_shape,
        num_resnet=1,
        num_hierarchies=3,
        # num_filters=32,
        num_filters=16,
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

    # model_dir = item_name("/gcohenlab/data/samuelgelman/data/non_equ_models/model_weights",p,secondary_keys, excluded_keys=['n_samples'])
    # model_dir = item_name("/home/sammy/gcohenlabfs/data/samuelgelman/data/ising_models/investigation",p,secondary_keys, excluded_keys=['n_samples'])
    model_dir = item_name("/gcohenlab/data/samuelgelman/data/ising_models/final_models",p,secondary_keys)
    # model_dir = item_name("/gcohenlab/data/samuelgelman/data/ising_models/take_1",p,secondary_keys)

    # for i in range(15):
    # model.load_weights(str(model_dir)+"/weights_{0}/cp.ckpt".format(epochs))
    model.load_weights(str(model_dir)+"/weights_27/cp.ckpt")
    

    start_time = time.perf_counter()

    # sample n images from the trained model
    print("Sampling...")
    # samples = dist.sample(n_samples)

    # # Plot samples:
    entropies = []

    for sample in samples_mc:
        entropies.append(dist.log_prob(sample['image'].numpy()).numpy())
        # s = sample.numpy()[:,:,0]

    print(entropies)

    entropy = sum(entropies)/(n_samples*L**2)*(-1)
    results.append(entropy)

    end_time = time.perf_counter()
    cnn_time = end_time - start_time

    with open('final_entropy.txt', 'a') as f:
        f.write(str(results[0])+'\n')
    f.close()

# with open('timer.txt', 'a') as f:
#     f.write(str('This is the pixelCNN time')+'\n'+str(cnn_time)+'\n')
# f.close()
#
#
# start_time = time.perf_counter()
#
# # Plot samples:
# entropies_mc = []
# for sample in samples_mc:
#     entropies_mc.append(dist.log_prob(sample).numpy())
#     s = sample.numpy()[:,:,0]
#
# entropy_mc =  sum(entropies_mc)/(n_samples*L**2)*(-1)
# results.append(entropy_mc)
# with open('entropy_mc.txt', 'a') as f:
#     f.write(str(results[0])+'\n')
# f.close()
#
# end_time = time.perf_counter()
# mc_time = end_time - start_time
#
# with open('timer.txt', 'a') as f:
#     f.write(str('This is the mc_samples time')+'\n'+str(mc_time)+'\n')
# f.close()


