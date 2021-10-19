import numpy as np
import configparser
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument('batches', type=int, nargs='+',
                    help='number of data realizations computed')
args = parser.parse_args()
batches = args.batches[0]

config = configparser.ConfigParser()
config.read("run.param")
T = float(config['input']['T'])
C = int(config['input']['C'])
H = float(config['input']['H'])

def batch_catcher(batches,T,H,C):
    sample_batches_rand = np.linspace(0,batches-1,batches)
    random.shuffle(sample_batches_rand)
    data_list = []
    for batch in sample_batches_rand:
        x = np.load('samples_rank'+str(int(batch))+'.npz')
        # x = time_extract('/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/samples_rank'+str(int(batch))+'.npz')
        data_list.append(x)
    return data_list

def slicer(C,data_list,cycle_lag):
    outputs = [ [] for _ in range(C) ]
    for d in data_list:
        for i, (l, s) in enumerate(d.items()):
            # print(f"time {i}, slice {i%C}")
            if i >= cycle_lag*C:
                outputs[i%C].append(s)

    for i in range(C):
        np.savez(f'slice_{i}.npz', *outputs[i])

data_list = batch_catcher(batches,T,H,C)
slicer(C,data_list,1)
