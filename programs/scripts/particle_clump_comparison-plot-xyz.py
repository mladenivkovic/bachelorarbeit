#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script will plot the clump(s) found by phew and estimated clump size along with all the particles found by me so I can compare.

# Usage: execute the corresponding bash script.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt


outputfilename = "particle_clump_comparison_plot-xyz"
title='Particle clump comparison plot'
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


def get_clump_data() :   
    print "Reading in cell data"
    for i in range(0,noutput):
        inputfile=str(argv[i+2+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[4,5,6,10])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

    return data[:,0], data[:,1], data[:,2], data[:,3]






def radius(mass):
    
    #Calculating the area of the halo for the scatterplot, assuming halo has density 200. Comes from M_halo = 4/3 pi * r^3 * 200
    radius = np.zeros(len(mass))
    print "calculating clump area"
    for i in range(0, len(mass)):
        calc = (3 * mass[i] / 800.0 * np.pi) **(1./3)
        radius[i] = calc
    #print radius
    return radius


########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

# get data
    x_clump, y_clump, z_clump, mass_clump = get_clump_data()
    x_part, y_part, z_part = get_particle_data()

# Calculate radius
    radius = radius(mass_clump)





    print "Creating figure"

# creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(16,16))

    ax1 = fig.add_subplot(331, aspect='equal')
    ax2 = fig.add_subplot(334, aspect='equal')
    ax3 = fig.add_subplot(337, aspect='equal')
    ax4 = fig.add_subplot(332, aspect='equal')
    ax5 = fig.add_subplot(335, aspect='equal')
    ax6 = fig.add_subplot(338, aspect='equal')
    ax7 = fig.add_subplot(333, aspect='equal')
    ax8 = fig.add_subplot(336, aspect='equal')
    ax9 = fig.add_subplot(339, aspect='equal')

    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)   
    ax4.set_xlim(0.00,1.00)
    ax4.set_ylim(0.00,1.00)   
    ax5.set_xlim(0.00,1.00)
    ax5.set_ylim(0.00,1.00)   
    ax6.set_xlim(0.00,1.00)
    ax6.set_ylim(0.00,1.00)   
    ax7.set_xlim(0.00,1.00)
    ax7.set_ylim(0.00,1.00)   
    ax8.set_xlim(0.00,1.00)
    ax8.set_ylim(0.00,1.00)   
    ax9.set_xlim(0.00,1.00)
    ax9.set_ylim(0.00,1.00)   


#setting up an empty scatterplot for pixel reference
    xedges=[0.000, 1.000]
    yedges=[0.000, 1.000]
    emptyscatter1=ax1.scatter(xedges, yedges, s=0.0)
    emptyscatter2=ax2.scatter(xedges, yedges, s=0.0)
    emptyscatter3=ax3.scatter(xedges, yedges, s=0.0)
    emptyscatter4=ax4.scatter(xedges, yedges, s=0.0)
    emptyscatter5=ax5.scatter(xedges, yedges, s=0.0)
    emptyscatter6=ax6.scatter(xedges, yedges, s=0.0)
    emptyscatter7=ax7.scatter(xedges, yedges, s=0.0)
    emptyscatter8=ax8.scatter(xedges, yedges, s=0.0)
    emptyscatter9=ax9.scatter(xedges, yedges, s=0.0)
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)      
    ax4.set_xlim(0.00,1.00)
    ax4.set_ylim(0.00,1.00)   
    ax5.set_xlim(0.00,1.00)
    ax5.set_ylim(0.00,1.00)   
    ax6.set_xlim(0.00,1.00)
    ax6.set_ylim(0.00,1.00)   
    ax7.set_xlim(0.00,1.00)
    ax7.set_ylim(0.00,1.00)   
    ax8.set_xlim(0.00,1.00)
    ax8.set_ylim(0.00,1.00)   
    ax9.set_xlim(0.00,1.00)
    ax9.set_ylim(0.00,1.00)   

    # Calculating the ratio of pixel-to-unit
    
    upright = ax1.transData.transform((1.0, 1.0))
    lowleft = ax1.transData.transform((0.0,0.0))
    x_to_pix_ratio = upright[0] - lowleft[0]
    y_to_pix_ratio = upright[1] - lowleft[1]
    # Take the mean value of the ratios because why not and there is smthg wrong 
    dist_to_pix_ratio = (x_to_pix_ratio + y_to_pix_ratio) / 2.0

# Calculate marker size
    clumpsize = np.zeros(len(radius))
    for i in range(0, len(radius)):
        calc = (radius[i]*dist_to_pix_ratio)**2
        clumpsize[i] = calc
   
    



#####################################
#####################################
# X-Y PLANE

# clumpfinder data

    ax1.scatter(x_clump, y_clump, s=clumpsize, alpha=0.6, lw=0)
    ax1.set_title("Clumpfinder plot", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')

#particle data
    # use alpha=0.1 for big simulation
    ax2.scatter(x_part, y_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax2.set_title("Particle plot", family='serif')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

#particle and clumpfinder data
    ax3.scatter(x_clump, y_clump, s=clumpsize, alpha=0.6, lw=0)
    ax3.scatter(x_part, y_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax3.set_title("Particles and Clumpfinder plot", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')


#####################################
#####################################
# Y-Z PLANE

# clumpfinder data

    ax4.scatter(y_clump, z_clump, s=clumpsize, alpha=0.6, lw=0)
    ax4.set_title("Clumpfinder plot", family='serif')
    ax4.set_xlabel('y')
    ax4.set_ylabel('z')

#particle data
    # use alpha=0.1 for big simulation
    ax5.scatter(y_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax5.set_title("Particle plot", family='serif')
    ax5.set_xlabel('y')
    ax5.set_ylabel('z')

#particle and clumpfinder data
    ax6.scatter(y_clump, z_clump, s=clumpsize, alpha=0.6, lw=0)
    ax6.scatter(y_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax6.set_title("Particles and Clumpfinder plot", family='serif')
    ax6.set_xlabel('y')
    ax6.set_ylabel('z')


#####################################
#####################################
# X-Z PLANE

# clumpfinder data

    ax7.scatter(x_clump, z_clump, s=clumpsize, alpha=0.6, lw=0)
    ax7.set_title("Clumpfinder plot", family='serif')
    ax7.set_xlabel('x')
    ax7.set_ylabel('z')

#particle data
    # use alpha=0.1 for big simulation
    ax8.scatter(x_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax8.set_title("Particle plot", family='serif')
    ax8.set_xlabel('x')
    ax8.set_ylabel('z')

#particle and clumpfinder data
    ax9.scatter(x_clump, z_clump, s=clumpsize, alpha=0.6, lw=0)
    ax9.scatter(x_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0)
    ax9.set_title("Particles and Clumpfinder plot", family='serif')
    ax9.set_xlabel('x')
    ax9.set_ylabel('z')


    
    fig.tight_layout()
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"
