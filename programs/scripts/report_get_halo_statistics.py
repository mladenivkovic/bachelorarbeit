#!/usr/bin/python

# Intended for cosmo runs
# Writes out halos, the number of children they have, the number of particles in the halo and in the children


from os import getcwd
from sys import argv #command line arguments
import numpy as np
import warnings
import matplotlib.pyplot as plt

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])





def get_parents(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+4]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0,2])
        if(len(np.atleast_1d(temp_data_int))>1):
            if 'clump_data' in locals():
                clump_data= np.vstack((clump_data, temp_data_int))
            else:
                clump_data = temp_data_int

    
    maxid_clump=max(clump_data[:,0]) #how many clumps

    for i in range(0,noutput):
        inputfile=str(argv[i+4+2*noutput]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0])
        # if(len(np.atleast_1d(temp_data_int))>0):# and temp_data_int.shape[0]>0):
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'halo_data' in locals():
                halo_data= np.concatenate((halo_data, temp_data_int))
            else:
                halo_data = temp_data_int

    if len(np.atleast_1d(halo_data))>1:
        maxid_halo=max(halo_data) #how many clumps
    else:
        maxid_halo=halo_data
        halo_data=np.array([halo_data])

    

    clumpnr=max((maxid_halo, maxid_clump))


    parents=[0]*(clumpnr+1)
    
    for k in range(clump_data.shape[0]):
        parents[int(clump_data[k,0])]=int(clump_data[k,1])

    for k in range(len(halo_data)):
        parents[int(halo_data[k])]=-1 #set halos to -1

   

    
    children = [[]]*(clumpnr+1)

    # get children lists
    for k, parent in enumerate(parents):
        while parent > 0 : # if its not a halo, add to all parents (of parents...) until you reach halo
            if len(children[parent])>0:
                children[parent].append(k)
            else:
                children[parent]=[k]
            parent = parents[parent]

            

    return parents,children



#================================
#================================
#================================

def get_particle_data(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[6])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data' in locals():
                data= np.concatenate((data, temp_data_int))
            else:
                data = temp_data_int

    ids=data
    return ids


#================================
#================================
#================================



        
        
        
        


if __name__ == "__main__":

    # get data

    parents,children=get_parents(noutput)
    N = len(parents)

    ids=get_particle_data(noutput)


    # create empty arrays
    # particles of clump i is nparticles[i]
    nparticles = [0]*N
    nsump = [0]*N


    # Count clumpparticles
    for i in ids:
        nparticles[int(i)] += 1



    
    for i, parent in enumerate(parents):
        if parent == -1: # clump is halo
            nchild = len(children[i])
            cp=0
            if nchild>0: # if halo has children
                for j in children[i]: # sum up children's particles
                    cp+=nparticles[j]
                nsump[i] = cp

    sortd = np.argsort(nsump)   # get sorted array

    # print interesting data
    for j in range(N):
        i = sortd[j]
        if parents[i] == -1:
            nchild = len(children[i])
            if nchild>0:
                #  if nparticles[i]<nsump[i]: # optional filter
                if nchild <9:
                    print ('{0:5}{1:8}{2:6}{3:4}{4:6}{5:8}{6:6}{7:8}'.format("Halo:",i," nc ",nchild," hp ", int(nparticles[i]), " cp ", int(nsump[i])))





