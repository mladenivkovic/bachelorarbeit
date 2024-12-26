#!/usr/bin/python

# Writes the halo mass function to file. Called by reportplot -mf
# 
from os import getcwd
from sys import argv #command line arguments
import numpy as np
import warnings

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "halo_mass_function"




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
        if(len(np.atleast_1d(temp_data_int))>0):# and temp_data_int.shape[0]>0):
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


    parents=np.zeros(clumpnr+1)
    
    for k in range(clump_data.shape[0]):
        parents[int(clump_data[k,0])]=clump_data[k,1]

    for k in range(len(halo_data)):
        parents[int(halo_data[k])]=int(halo_data[k])

    #find which halo subclumps belong to
    for k in range(clump_data.shape[0]):
        ind=int(clump_data[k,0])
        p=int(clump_data[k,1])
        if parents[p]!=p: #if p is not halo
            nothalo=True
            while(nothalo):
                p=parents[p]
                nothalo=(p!=parents[p])

            parents[ind]=p

    return parents



#================================
#================================
#================================

def get_particle_data(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[6,8])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'data' in locals():
                data= np.concatenate((data, temp_data_int))
            else:
                data = temp_data_int

    ids=data[:,0]
    mass=data[:,1]
    return mass,ids


#================================
#================================
#================================

def get_mass_function(parents,mass,ids):
  
    halo_particles=np.zeros(len(parents))
    mass_threshold=0

    for i in range(len(ids)):
        if mass[i]>mass_threshold:
            ind=int(ids[i])
            pind=int(parents[ind])
            halo_particles[pind]+=1


    nbins=1
    i=1
    npart=100
    width=npart
    while(width<np.max(halo_particles)):
        nbins+=1 
        i+=1
        width=npart*2**i
    
    nbins+=1

    bins=np.zeros(nbins)
    values=np.zeros(nbins)
    for i in range(nbins):
        bins[i]=100.0*2**i

    for i in range(len(halo_particles)):
        if halo_particles[i]>0:
            ibin=0
            if bins[ibin]<halo_particles[i]:
                while(bins[ibin]<halo_particles[i]):
                    ibin+=1
            values[ibin]+=1


    return bins, values


def get_plot_values(bins,values):
    nbins=2*len(bins)+1
    i=2
    c=0
    plotbins=np.zeros(nbins)
    plotvalues=np.zeros(nbins)
    while(c<len(values)-1):  #-1 because index shift
        plotbins[i]=bins[c]
        plotvalues[i]=values[c]
        plotbins[i+1]=bins[c]
        plotvalues[i+1]=values[c+1]
        i+=2
        c+=1
    plotbins[i]=bins[c]
    plotvalues[i]=values[c]
    plotbins[0]=0
    plotbins[1]=0
    plotvalues[0]=0
    plotvalues[1]=values[0]
   
    return plotbins, plotvalues
        
        
        
        


if __name__ == "__main__":

    # # get data

    parents=get_parents(noutput)
    mass,ids=get_particle_data(noutput)
    bins,values=get_mass_function(parents,mass,ids)
    plotbins,plotvalues=get_plot_values(bins,values)

    print "writing data to file."
    fname=workdir+'/'+outputfilename+'.txt'
    f=open(fname,'w')
    for i in range(len(plotbins)):
        dat='{0:18d}{1:18d}'.format(int(plotbins[i]),int(plotvalues[i]))
        f.write(dat)
        f.write("\n")

    f.close()


    # fig = plt.figure(facecolor='white', figsize=(10,10))
    # ax1 = fig.add_subplot(111)#, aspect='equal')
    # ax1.loglog(plotbins,plotvalues)
    # # ax1.set_xlim(-1,2000000)
    # # ax1.set_ylim(-0.1,1.1)
    # plt.show()



