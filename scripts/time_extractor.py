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

def time_extract(t,t_cycle,filename):
    raw_data =  np.load(filename)
    r_data_list = []
    for sample in raw_data.files:
        r_data_list.append(raw_data[sample])
    r_data = np.array(r_data_list)

    t_data = []
    for count in range(len(r_data)):
        if (count % t_cycle) == t:
            t_data.append(r_data[count])

    return np.array(t_data)

def batch_catcher(batches,T,H,C):
    sample_batches_rand = np.linspace(0,batches-1,batches)
    random.shuffle(sample_batches_rand)
    data_list = []
    for batch in sample_batches_rand:
        x = time_extract(batch,C,'samples_rank'+str(int(batch))+'.npz')
        # x = time_extract(batch,C,'/gcohenlab/data/samuelgelman/data/non_equ_data/non_equilibrium_samples_H'+str(H)+'/T'+str(T)+'/samples_rank'+str(int(batch))+'.npz')
        for ix in x:
            data_list.append(ix)
    data = np.array(data_list)
    return data

def t_files(batches,T,H,C):
    t_scape = np.linspace(0,C-1,C)
    for time in t_scape:
        data = batch_catcher(batches,T,H,C)
        print(np.shape(data[0]))
        exit()
        np.savez('t'+str(time)+'_samples', *data)

t_files(batches,T,H,C)
