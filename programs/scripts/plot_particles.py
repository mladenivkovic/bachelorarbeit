#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script plots all particles that are in clumps. It makes 3 subplots,
# one for each plane of coordinates: xy, yz and xz
# 
# Usage: plot_particles.py <nproc> <mladen_clumpparticles.txt00*>
# <nproc> : number of processors used in ramses run, also the number of 
# output files
# <mladen_clumpparticles.txt00*>: all mladen_clumpparticles.txt* files.
# 
from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt


outputfilename = "clumpparticle_plot"
workdir= str(getcwd())

noutput=int(argv[1])


def get_particle_data():
    print "Reading in particle data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

    # filter out all non-clump particles
   
    counter=0
    for i in range(0, data.shape[0]):
        if (data[i,3]>0):
            counter+=1
            # print "got one"
    print "total particles", len(data)
    print "clumpparticles", counter

    # filteredx=np.zeros(counter)
    # filteredy=np.zeros(counter)
    # filteredz=np.zeros(counter)
    filteredx=[]
    filteredy=[]
    filteredz=[]


    for i in range(data.shape[0]):
        if (data[i,3]>0):
            
            filteredx.append(data[i,0])
            filteredy.append(data[i,1])
            filteredz.append(data[i,2])
            
    
    return filteredx, filteredy, filteredz 




########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

# get data
    x_part, y_part, z_part = get_particle_data()

    print "Creating figure"

# creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(16,6))
    fig.suptitle('Particle Plot - clumpparticles only', family='serif', size=20)
    ax1 = fig.add_subplot(131, aspect='equal')
    ax2 = fig.add_subplot(132, aspect='equal')
    ax3 = fig.add_subplot(133, aspect='equal')

    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)   
 


#####################################
#####################################
# X-Y PLANE

    # use alpha=0.1 for big simulation
    ax1.scatter(x_part, y_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax1.set_title("x-y plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')


#####################################
#####################################
# Y-Z PLANE


    ax2.scatter(y_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax2.set_title("y-z plane", family='serif')
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')


#####################################
#####################################
# X-Z PLANE

# clumpfinder data

#particle and clumpfinder data
    ax3.scatter(x_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax3.set_title("x-z plane", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')


    
    fig.tight_layout()
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"
