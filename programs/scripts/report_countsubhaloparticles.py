#!/usr/bin/python

# Counts the number of sarticles that are in subhalos


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
   
    clump_data=np.array([])
    halo_data=np.array([])

    for i in range(0,noutput):
        inputfile=str(argv[i+4+2*noutput]) 
        print "halos: reading", inputfile


        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                temp_data_halo=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0])

            if np.atleast_1d(halo_data).shape[0] >0:
                halo_data = np.concatenate((np.atleast_1d(halo_data), np.atleast_1d(temp_data_halo)))
            else:
                halo_data = np.copy(temp_data_halo)

            # if halo_data.size >0:
            #     halo_data= np.concatenate((halo_data, temp_data_int))
            # else:
            #     halo_data = np.copy(temp_data_int)

        except ValueError:
            pass

        inputfile=str(argv[i+4]) 
        print "clumps: reading", inputfile
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                temp_data_clump=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0])

            if np.atleast_1d(clump_data).shape[0] >0:
                clump_data = np.concatenate((np.atleast_1d(clump_data), np.atleast_1d(temp_data_clump)))
            else:
                clump_data = np.copy(temp_data_clump)

        except ValueError:
            pass

    return halo_data, clump_data



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

    halos,clumps=get_parents(noutput)
    ids=get_particle_data(noutput)
    print len(halos), len(clumps)

    if len(halos) < 10:

        N = len(clumps)
        nclump = [0]*N
        nnone = 0
        
        ntot = float(len(ids))
        nhalo = 0
        nsub = 0


        for i in ids:
            if i > 0:
                for j,clump in enumerate(clumps):
                    if i == clump:
                        nclump[j]+=1
                        break
                        
            else:
                nnone += 1
        

        for i,c in enumerate(clumps):
            which = 'Subhalo'
            if c in halos:
                which = 'Halo   '
                nhalo += nclump[i]
            else:
                nsub += nclump[i]

            print which, c, "particles:", nclump[i]


        print "----------------------"
        print("{0:30}{1:10}{2:8}{3:10.9f}".format( "Total particles in halos:    ", nhalo , " ratio: ", nhalo/ntot))
        print("{0:30}{1:10}{2:8}{3:10.9f}".format( "Total particles in subhalos: ", nsub  , " ratio: ", nsub/ntot))
        print("{0:30}{1:10}{2:8}{3:10.9f}".format( "Total particles in no halos: ", nnone , " ratio: ", nnone/ntot))
        print("{0:30}{1:10}".format( "Total particles:             ", int(ntot ) ))


    else:
        nsub = 0
        nhalo = 0
        nnone = 0

        for i in ids:
            if i>0:
                if i in halos:
                    nhalo+=1
                else:
                    nsub+=1
            else:
                nnone+=1

        ntot = nsub + nhalo + nnone

        print "Sub:", nsub, "halo:", nhalo, "none:", nnone, "total:", ntot, "ratio:", nsub/float(ntot)


     


