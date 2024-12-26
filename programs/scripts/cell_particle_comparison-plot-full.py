#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script will plot the clump(s) found by phew and estimated clump size along with all the particles found by me so I can compare.

# Usage: execute the corresponding bash script.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt


outputfilename = "cell_particle_comparison_plot-full"
title='Cell particle comparison plot'
workdir= str(getcwd())

noutput=int(argv[1])

def get_particle_data():
    print "Reading in particle data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2]) 
        print "reading from", inputfile
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[1,2])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)
    print data[0,:]
    return data[:,0], data[:,1]


def get_cell_data() :   
    print "Reading in cell data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

    return data[:,0], data[:,1]

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    print "cell_particle_comparison-plot.py called"

    xp, yp=get_particle_data()
    xc, yc=get_cell_data()

    print "Creating figure"


    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,32))
    fig.suptitle(title, family='serif', size=20) 
    ax1 = fig.add_subplot(311, aspect='equal', clip_on=True)
    ax2 = fig.add_subplot(312, aspect='equal')
    ax3 = fig.add_subplot(313, aspect='equal')


    # Plot it
    ax1.scatter(xc, yc, s=1, alpha=0.3, lw=0, marker='s', color='b')
    ax1.set_title("Cell Positions", family='serif')
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   





    #############################
    #PARTICLE DATA
    # second subplot
    # use alpha=0.1 for big simulation
    ax2.scatter(xp, yp, s=0.15, color='red', alpha=1, marker=",", lw=0)
    ax2.set_title("Particle plot", family='serif')
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   

    #############################
    #PARTICLE AND CLUMPFINDER DATA
    # third subplot
    ax3.scatter(xc, yc, s=1, alpha=0.3, lw=0, marker='s', color='b')
    ax3.scatter(xp, yp, s=0.15, color='red', alpha=1, marker=",", lw=0)
    ax3.set_title("Particles and Clumpfinder plot", family='serif')
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)  






    

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=200)
    plt.close()

    print "done", outputfilename+".png"
