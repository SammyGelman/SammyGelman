import numpy as np
import configparser
import argparse
import random
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
T = float(config['input']['T'])
# C = int(config['input']['C'])
# H = float(config['input']['H'])
C=50
H=1
def batch_catcher(batches,T,H,C,prefix):
    sample_batches_rand = np.linspace(0,batches-1,batches)
    random.shuffle(sample_batches_rand)
    data_list = []
    for batch in sample_batches_rand:
        x = np.load("/home/sammy/gcohenlabfs/data/samuelgelman/data/non_equ_data/phase_diagram_data/"+str(prefix)+"/samples_rank"+str(int(batch))+".npz")
        data_list.append(x)
    return data_list

def slicer(C,data_list,cycle_lag,prefix):
    outputs = [ [] for _ in range(C) ]
    for d in data_list:
        for i, (l, s) in enumerate(d.items()):
            # print(f"time {i}, slice {i%C}")
            if i >= cycle_lag*C:
                outputs[i%C].append(s)
    for i in range(C):
        np.savez(f'{prefix}/slice_{i}.npz', *outputs[i])

for direc in dirs:
    # config.read(str(dirs[i])+"/run.param")
    # T = float(config['input']['T'])
    # C = int(config['input']['C'])
    # H = float(config['input']['H'])

    data_list = batch_catcher(batches,T,H,C,direc)
    slicer(C,data_list,1,direc)
