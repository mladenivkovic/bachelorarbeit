#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt




def get_particle_data(noutput):
    print "Reading in particle data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6])
        if (temp_data.shape[0]>0):
            if 'data' in locals():
                data = np.concatenate((data, temp_data), axis=0)
            else:
                data = temp_data

    # filter out all non-clump particles
   
    counter=0
    for i in range(0, data.shape[0]):
        if (data[i,3]>0):
            counter+=1
            # print "got one"

    print "counter", counter

    filteredx=np.zeros(counter)
    filteredy=np.zeros(counter)
    filteredz=np.zeros(counter)

    ind=0
    for i in range(data.shape[0]):
        if (data[i,3]>0):
            
            filteredx[ind]=data[i,0]
            filteredy[ind]=data[i,1]
            filteredz[ind]=data[i,2]
            ind+=1
            
    
    return filteredx, filteredy, filteredz 




########################################################################
########################################################################
########################################################################
########################################################################


