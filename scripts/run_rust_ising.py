#!/usr/bin/env python
import os
import configparser

config = configparser.ConfigParser()
config.read('run.param')
exec_file = "/gcohenlab/data/samuelgelman/src/rust_ising/target/release/rust_ising"
help = """
ising model runner.

USAGE:
    rust_ising [FLAGS] [OPTIONS]

FLAGS:
    -h, --help               Prints help information
    -V, --version            Prints version information
    -W, --wolff-algorithm    Use Wolff (as opposed to Metropolis) algorithm
    -w, --write-samples      Output samples to file

OPTIONS:
    -d, --decorrelation-steps <decorrelation-steps>    Decorrelation steps [default: -1]
    -e, --equilibration-steps <equilibration-steps>    Equilibration steps [default: 100]
    -J, --interaction <interaction>                    Interaction strength [default: 1.0]
    -l, --lattice-size <lattice-size>                  Lattice size [default: 16]
    -H, --magnetic-field <magnetic-field>              Magnetic field strength [default: 0.0]
    -r, --random-seed <random-seed>                    Random seed
    -s, --samples <samples>                            Number of samples [default: 100]
    -T, --temperature <temperature>                    Temperature [default: 1.0]
"""

l = int(config['input']['l'])
T = float(config['input']['T'])
s = int(config['input']['s'])
e = int(config['input']['e'])
d = int(config['input']['d'])
# run_string = "mpirun " + exec_file + f" -s={s} -l={l} -T={T} -d={d} -e={e} -w -W"
run_string = "mpirun " + exec_file + f" -s={s} -l={l} -T={T} -d={d} -e={e} -w"

print(run_string)

os.system(run_string)
