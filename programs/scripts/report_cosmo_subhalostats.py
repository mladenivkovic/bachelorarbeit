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





def get_halos(noutput):
#     for i in range(0,noutput):
        # inputfile=str(argv[i+4]) 
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        #     temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0,2])
        # if(len(np.atleast_1d(temp_data_int))>1):
        #     if 'clump_data' in locals():
        #         clump_data= np.vstack((clump_data, temp_data_int))
        #     else:
        #         clump_data = temp_data_int
# 
    
    # maxid_clump=max(clump_data[:,0]) #how many clumps

    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
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
    

    clumpnr=int(max(halo_data)*1.1)
    # clumpnr=max((maxid_halo, maxid_clump))


    ishalo=[0]*(clumpnr+1)
    
    # for k in range(clump_data.shape[0]):
    #     if clump_data[k,1] == clump_data[k,0]:
    #         ishalo[int(clump_data[k,0])]=1

    for k in halo_data:
        ishalo[k]=1 #set halos to 1

   

    
#     children = [[]]*(clumpnr+1)
    # 
    # # get children lists
    # for k, parent in enumerate(parents):
    #     while parent > 0 : # if its not a halo, add to all parents (of parents...) until you reach halo
    #         if len(children[parent])>0:
    #             children[parent].append(k)
    #         else:
    #             children[parent]=[k]
    #         parent = parents[parent]
# 
            

    return ishalo #,children



#================================
#================================
#================================

def get_particle_data(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+4+2*noutput]) 
        print "particles: reading", inputfile
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[6])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data' in locals():
                data= np.concatenate((data, temp_data_int))
            else:
                data = np.copy(temp_data_int)

    ids_iter=data
    
    for i in range(0,noutput):
        inputfile=str(argv[i+4+3*noutput]) 
        print "particles: reading", inputfile
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int2=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[6])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data2' in locals():
                data2= np.concatenate((data2, temp_data_int2))
            else:
                data2 = np.copy(temp_data_int2)

    ids_saddle=data2

    return ids_iter, ids_saddle


#================================
#================================
#================================



        
        
        
        


if __name__ == "__main__":

    # get data

    ishalo=get_halos(noutput)
    N = len(ishalo)

    ids_iter, ids_saddle=get_particle_data(noutput)


    # create empty arrays
    # particles of clump i is nparticles[i]
    nparticles_i = [0]*N
    nparticles_s = [0]*N


    # Count clumpparticles
    for i in ids_iter:
        nparticles_i[int(i)] += 1
    for i in ids_saddle:
        nparticles_s[int(i)] += 1
   

    
#     for i, parent in enumerate(parents):
        # if parent == -1: # clump is halo
        #     nchild = len(children[i])
        #     cp=0
        #     if nchild>0: # if halo has children
        #         for j in children[i]: # sum up children's particles
        #             cp+=nparticles[j]
        #         nsump[i] = cp
        # 
    # sortd = np.argsort(nsump)   # get sorted array

    # print interesting data
    nless=0
    nsame=0
    nmore=0
    npartmore=0
    npartless=0

    # nsub_i=0
    # nsub_s=0
    for i in range(1,N):
        # i = sortd[j]
        if ishalo[i] == 0:
            if nparticles_i[i] + nparticles_s[i]>0:
                if nparticles_i[i] < nparticles_s[i]:
                    # print "clump", i, ": diff", nparticles_i[i]-nparticles_s[i]
                    nless+=1
                    npartless+=nparticles_s[i]-nparticles_i[i]
                elif nparticles_i[i] > nparticles_s[i]:
                    nmore+=1
                    npartmore+=nparticles_i[i]-nparticles_s[i]
                else:
                    nsame+=1
    print "Iter run has less:", nless, "more:", nmore, "same:", nsame, "more particles:", npartmore, "less particles:", npartless, "total:", npartmore-npartless


            # nsub_i+=nparticles_i[i]
            # nsub_s+=nparticles_s[i]
    # print "iter:", nsub_i, "saddle:", nsub_s






