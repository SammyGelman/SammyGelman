#!/usr/bin/env python
#Build a small Pixel CNN++ model to train on MNIST.

import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
import numpy as np
from dataset_prep import like_mnist
import pickle
import os
import configparser
# import matplotlib.pyplot as plt
# parser = argparse.ArgumentParser()
# parser.add_argument('temprature', type=float, nargs='+',
#                     help='temperature of 0.5 increments')
# parser.add_argument('length', type=int, nargs='+',
#                     help='size of lattice')
# parser.add_argument('checkpoints',type=str, default ='None',
#                     help='this is a path to the directory containing the pretrained weights')
# parser.add_argument('epochs',type=int, default ='None',
#                     help='these are the epochs')
# args = parser.parse_args()
#
# T = args.temprature[0]
# L = args.length[0]
# cp_path = args.checkpoints
# epochs = args.epochs[0]

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

tfd = tfp.distributions
tfk = tf.keras
tfkl = tf.keras.layers

# tf.enable_v2_behavior()
results = []

#trying my dataset out
image_shape, data = like_mnist(T,L)
# Load MNIST from tensorflow_datasets
# data = tfds.load('mnist')
# train_data, test_data = data['train'], data['test']
# print(train_data,test_data)
# data = data.shuffle(shuffbuff)
train_data = data.take(training_samples)
# train_data = train_data.take(1000)
test_data = data.skip(training_samples).take(test_samples)
# test_data = test_data.take(1000)

def image_preprocess(x):
    x['image'] = tf.cast(x['image'], tf.float32)
    return (x['image'],)  # (input, output) of the model

train_it = train_data.map(image_preprocess).batch(batch_size).shuffle(shuffbuff)


# image_shape = (28,28, 1)
# image_shape = shape
# Define a Pixel CNN network
dist = tfd.PixelCNN(
    image_shape=image_shape,
    num_resnet=1,
    num_hierarchies=heirarchies,
    num_filters=filters,
    num_logistic_mix=logistic_mix,
    dropout_p=dropout,
    high=1
)

# Define the model input
image_input = tfkl.Input(shape=image_shape)

# Define the log likelihood for the loss fn
log_prob = dist.log_prob(image_input)

# Define the model
model = tfk.Model(inputs=image_input, outputs=log_prob)
model.add_loss(-tf.reduce_mean(log_prob))

# Compile and train the model
if T<=1:
    model.compile(
        optimizer=tfk.optimizers.Adam(learning_rate/4),
        metrics=[])
elif T>=4:
    model.compile(
        optimizer=tfk.optimizers.Adam(learning_rate*3),
        metrics=[])
else:
    model.compile(
        optimizer=tfk.optimizers.Adam(learning_rate),
        metrics=[])

# Save weights to  checkpoint file
checkpoint_path = "weights/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
print(checkpoint_dir)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                save_weights_only=True,
                                                verbose=1)
print("Fitting...")
H = model.fit(train_it,
          epochs=epochs,
          verbose=2,
          validation_data=test_it,
          callbacks=[cp_callback])  # Pass callback to training

# save training loss
# loss = np.zeros((2,epochs)) 
# loss[0,:], loss[1,:] = np.arange(0, epochs), H.history["loss"]
np.savetxt('loss.dat',np.c_[loss[0,:],loss[1,:]])
np.savetxt('validation_loss.dat',H.history["val_loss"])
