#!/usr/bin/python
#find the most and leas massive particle. Usage: maxmass.py mladen_particleoutput*
import numpy as np
from sys import argv #command line arguments
import warnings

def get_data(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+1]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[8])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data' in locals():
                data= np.concatenate((data, temp_data_int))
            else:
                data = temp_data_int

    print "max: ", max(data), " min: ", min(data)
    return 



if __name__=='__main__':

    noutput=len(argv)-1
    get_data(noutput)
