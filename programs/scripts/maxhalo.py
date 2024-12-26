#!/usr/bin/python
#Find most massive halo and its index. 
#Usage: maxhalo.py halo_*
import numpy as np
from sys import argv #command line arguments
import warnings

def get_data(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+1]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data' in locals():
                data= np.vstack((data, temp_data_int))
            else:
                data = temp_data_int

    if len(data)==data.shape[0]:
        data=np.array([data])

    halo=data[0][:,0]
    print halo
    mass=data[0][:,1]
    ind=np.argmax(mass)
    print 'most massive halo: ', int(halo[ind]), ' mass: ', mass[ind]
    return 



if __name__=='__main__':

    noutput=len(argv)-1
    get_data(noutput)
