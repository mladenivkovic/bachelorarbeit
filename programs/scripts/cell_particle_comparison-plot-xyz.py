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


outputfilename = "cell_particle_comparison_plot-xyz"
title='Cell particle comparison plot'
workdir= str(getcwd())

noutput=int(argv[1])

def get_particle_data():
    print "Reading in particle data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[1,2,3])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

    return data[:,0], data[:,1], data[:,2]


def get_cell_data() :   
    print "Reading in cell data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

    return data[:,0], data[:,1], data[:,2], data[:,3]

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    print "cell_particle_comparison-plot-xyz.py called"

    xp, yp, zp=get_particle_data()
    xc, yc, zc, cellsize=get_cell_data()

    print "Creating figure"


    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(16,6))
    fig.suptitle(title, family='serif', size=20) 
    ax1 = fig.add_subplot(131, aspect='equal', clip_on=True)
    ax2 = fig.add_subplot(132, aspect='equal')
    ax3 = fig.add_subplot(133, aspect='equal')

    #setting up an empty scatterplot for pixel reference
    xedges=[0.000, 1.000]
    yedges=[0.000, 1.000]
    emptyscatter1=ax1.scatter(xedges, yedges, s=0.0)
    emptyscatter2=ax2.scatter(xedges, yedges, s=0.0)
    emptyscatter3=ax3.scatter(xedges, yedges, s=0.0)
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)   

    upright1 = ax1.transData.transform((1.0, 1.0))
    lowleft1 = ax1.transData.transform((0.0,0.0))
    x_to_pix_ratio1 = upright1[0] - lowleft1[0]
    y_to_pix_ratio1 = upright1[1] - lowleft1[1]
    # Take the mean value of the ratios because why not 
    #dist_to_pix_ratio1 = (x_to_pix_ratio1 + y_to_pix_ratio1) / 2.0
    #dist_to_pix_ratio1=x_to_pix_ratio1
    size= cellsize*x_to_pix_ratio1*y_to_pix_ratio1

    #compute cellsize
    #size=cellsize*dist_to_pix_ratio1**2

    # Plot it
    ax1.scatter(xc, yc, s=size, alpha=0.3, lw=0, marker='s', color='b')
    ax1.scatter(xp, yp, s=0.15, color='red', alpha=1, marker=",", lw=0)
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')


    #############################
    #PARTICLE DATA
    # second subplot
    # use alpha=0.1 for big simulation
    ax2.scatter(yc, zc, s=size, alpha=0.3, lw=0, marker='s', color='b')
    ax2.scatter(yp, zp, s=0.15, color='red', alpha=1, marker=",", lw=0)
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    
    #############################
    #PARTICLE AND CLUMPFINDER DATA
    # third subplot
    ax3.scatter(xc, zc, s=size, alpha=0.3, lw=0, marker='s', color='b')
    ax3.scatter(xp, zp, s=0.15, color='red', alpha=1, marker=",", lw=0)
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)  
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')




    print "Figure created"
    
    plt.tight_layout()
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"
