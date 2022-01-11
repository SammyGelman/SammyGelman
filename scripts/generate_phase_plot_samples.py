import os
import numpy as np
import argparse
import configparser

# parser = argparse.ArgumentParser()
# parser.add_argument('length', type=int, nargs='+',
#                     help='size of lattice')
# args = parser.parse_args()
# l = args.length[0]

config = configparser.ConfigParser()
config.read("run.param")
l = int(config['input']['L'])

T = np.around(np.linspace(0.0,4.0,41),decimals=1)
H = np.around(np.linspace(0.0,4.0,41),decimals=1)

for t in T:
    for h in H:
        os.system('mpirun /gcohenlab/data/samuelgelman/src/rust_ising/target/release/glauber -s 5000 -l %s -C 50 -H %s -T %s > "T%s_H%s.dat"' % (l,h,t,t,h))


