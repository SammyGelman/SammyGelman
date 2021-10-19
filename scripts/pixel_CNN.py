#!/usr/bin/env python
#Build a small Pixel CNN++ model to train on MNIST.

import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_probability as tfp
import numpy as np
from dataset_prep import like_mnist
import pickle
import os
import argparse
import configparser

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
cp_path = str(config['input']['cp'])

tfd = tfp.distributions
tfk = tf.keras
tfkl = tf.keras.layers

# tf.enable_v2_behavior()
results = []

#trying my dataset out
shape, data = like_mnist(T,L)

# Load MNIST from tensorflow_datasets
# data = tfds.load('mnist')
# train_data, test_data = data['train'], data['test']
# print(train_data,test_data)
data = data.shuffle(1000)
train_data = data.take(5000)
# train_data = train_data.take(1000)
test_data = data.take(500)
# test_data = test_data.take(1000)

def image_preprocess(x):
    x['image'] = tf.cast(x['image'], tf.float32)
    return (x['image'],)  # (input, output) of the model

batch_size = 16
train_it = train_data.map(image_preprocess).batch(batch_size).shuffle(1000)


# image_shape = (28,28, 1)
image_shape = shape
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

# Compile and train the model
model.compile(
    optimizer=tfk.optimizers.Adam(.001),
    metrics=[])

# Generate new weights or load pre-existing ones
if cp_path == 'None':
    checkpoint_path = "weights/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                    save_weights_only=True,
                                                    verbose=1)
    print("Fitting...")
    H = model.fit(train_it,
              epochs=epochs,
              verbose=True,
              callbacks=[cp_callback])  # Pass callback to training
else:
    model.load_weights(str(cp_path)+"/cp.ckpt")

# sample n images from the trained model
n = 3
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

entropy =  sum(entropies)/(n*shape[1]**2)*(-1)
results.append(entropy)
print(results)
with open('entropy_T'+str(T)+'.txt', 'a') as f:
    f.write(str(results[0])+'\n')
f.close()

# plot the training loss and accuracy
N = epochs
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.title("Training Loss: T="+str(T)+", l="+str(L))
plt.xlabel("Epoch #")
plt.ylabel("Loss")
plt.legend(loc="lower left")
plt.savefig("learning_curve.pdf")
