#!/usr/bin/env python 
import pandas as pd

#for this filename = 'entropy.txt'
#for this output_key = 'entropy'

def fill_df(globber='T*/',output_key='entropy',output_file='entropy.txt'):
    import glob
    import configparser
    """
    params:
    globber: type=string. key to place in glob to
        Key History: 'T*/*/'
    output_column: type=string. Desired column fill.
        History: 'entropy'
    output_file: type=string. File in which to fill
        History: 'entropy.txt'
    """
    direc = glob.glob(globber)
    config = configparser.ConfigParser()
    config.read(direc[0]+"/run.param")
    keys = list(config['input'].keys())
    keys.append(output_key)
    data = {key : [] for key in keys}

    # What we have going into this is a dictionary filled with lists that we can
    # add the contents of all our outpus that are scattered through many
    # directories. The list of directories is already compiled. What needs to be
    # done now is it iterate over the values found in all of those directories and
    
    # put the data in the respective keys.
    #For loops iterete over keys. So if I run a for loop through my run.param
    #dictionary, I can grab the key name and find the value, and then append it to
    #the list.  So in order to do this I need to make run.param into a readable
    #dict. Then I need to find out how to get a value of a specific key.

    for i in range(len(direc)):
        config.read(direc[i]+"run.param")
        run_dict = {s:dict(config.items(s)) for s in config.sections()}
        run_dict = list(run_dict.values())[0]

        #put run.param data in 'data' list dictionary

        for key in run_dict:
            data[key].append(run_dict[key])

        #read output data and append to 'data'

        output_dir = direc[i]+output_file
        output_val = float(open(output_dir,"r").read())
        data[output_key].append(output_val)

    dataframe = pd.DataFrame(data)
    #only keep temp
    t_data = dataframe[['t', output_key]]
    t_data = t_data.sort_values('t')
    return(t_data)

if __name__ == '__main__':
    pass
