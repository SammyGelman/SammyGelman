#!/usr/bin/env python
import numpy as np
import pickle
import random
import configparser
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('batches', type=int, nargs='+',
                    help='number of data realizations computed')
parser.add_argument('dirs', type=str, nargs='+',
                    help='directory prefix to time extract from')

args = parser.parse_args()
batches = args.batches[0]
prefix = args.dirs[0]

dirs = [s for s in os.listdir() if s.startswith(prefix)]

config = configparser.ConfigParser()
config.read(str(dirs[0])+"/run.param")
# T = float(config['input']['T'])
L = int(config['input']['L'])

def melder(data_list):
    outputs = []
    final_output = []
    for d in data_list:
        for i, (l,s) in enumerate(d.items()):
            outputs.append([s])
    for i in range(len(outputs)):
        final_output.append(outputs[i][0]) 
    return final_output

def batch_catcher(batches,prefix):
    sample_batches_rand = np.linspace(0,batches-1,batches)
    random.shuffle(sample_batches_rand)
    data_list = []
    for batch in sample_batches_rand:
        # x = np.load('samples_rank'+str(int(batch))+'.npz')
        # x = time_extract('/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/samples_rank'+str(int(batch))+'.npz')
        # x = np.load("/home/sammy/gcohenlabfs/data/samuelgelman/data/non_equ_data/phase_diagram_data/"+str(prefix)+"/samples_rank"+str(int(batch))+".npz")
        x = np.load("/home/sammy/gcohenlabfs/data/samuelgelman/data/ising_data/ising_samples_l"+str(L)+"/"+str(prefix)+"/samples_rank"+str(int(batch))+".npz")
        data_list.append(x)
    return data_list

for direc in dirs:
    data_list = batch_catcher(batches,direc)
    samples = melder(data_list)
    np.savez(str(direc)+"/final_samples.npz",*samples[:len(samples)])
