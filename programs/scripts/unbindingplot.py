#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script plots all particles that are in clumps and mark the ones 
# that were unbound. It makes 3 subplots,
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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend


outputfilename = "unbinding_plot"
workdir= str(getcwd())

noutput=int(argv[1])
particles=int(argv[2])

fontP=FontProperties()
fontP.set_size('x-small') 


def get_particle_data():
    print "Reading in particle data"
    particle_index=0
    data=np.zeros((particles,5))
    for i in range(0,noutput):
        inputfile=str(argv[i+3]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6,7])
        if (temp_data.shape[0]>0):
            for j in range(temp_data.shape[0]):
                for k in range(5):
                    data[j+particle_index,k]=temp_data[j,k]
        
            particle_index=particle_index+temp_data.shape[0]-1

    # filter out all non-clump particles
    filteredx=np.zeros(particles)
    filteredy=np.zeros(particles)
    filteredz=np.zeros(particles)
    unboundx=np.zeros(particles)
    unboundy=np.zeros(particles)
    unboundz=np.zeros(particles)
    fc=0
    uc=0
    for i in range(data.shape[0]):
        if (data[i,3]>0):
            filteredx[fc]=data[i,0]  
            filteredy[fc]=data[i,1]
            filteredz[fc]=data[i,2] 
            fc+=1
            if (data[i,4]>0):
                unboundx[uc]=data[i,0]
                unboundy[uc]=data[i,1]
                unboundz[uc]=data[i,2]
                uc+=1


    fx=np.zeros(fc)
    fy=np.zeros(fc)
    fz=np.zeros(fc)
    for i in range(fc):
        fx[i]=filteredx[i]
        fy[i]=filteredy[i]
        fz[i]=filteredz[i]
            
    ux=np.zeros(uc)
    uy=np.zeros(uc)
    uz=np.zeros(uc)
    for i in range(uc):
        ux[i]=unboundx[i]
        uy[i]=unboundy[i]
        uz[i]=unboundz[i]
  
    return fx, fy, fz, ux, uy, uz 




########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

# get data
    x_part, y_part, z_part, x_unb, y_unb, z_unb = get_particle_data()

    print "Creating figure"

# creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(16,6))
    fig.suptitle('unbinding plot', family='serif', size=20)
    ax1 = fig.add_subplot(131, aspect='equal')
    ax2 = fig.add_subplot(132, aspect='equal')
    ax3 = fig.add_subplot(133, aspect='equal')

    # ax1.set_xlim(0.00,1.00)
    # ax1.set_ylim(0.00,1.00)   
    # ax2.set_xlim(0.00,1.00)
    # ax2.set_ylim(0.00,1.00)   
    # ax3.set_xlim(0.00,1.00)
    # ax3.set_ylim(0.00,1.00)   
 


#####################################
#####################################
# X-Y PLANE

    # use alpha=0.1 for big simulation
    ax1.scatter(x_part, y_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0, label='clumpparticles')
    ax1.scatter(x_unb, y_unb, s=0.1, color='blue', alpha=0.5, marker=",", lw=0, label='particles unbound from substructure')
    ax1.set_title("x-y plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP)#,scatteryoffsets=[5,5,5,5])
    for l in range(2): #range 3: exactly as many as there are labelled plots!
        lgnd1.legendHandles[l]._sizes = [20]



#####################################
#####################################
# Y-Z PLANE


    ax2.scatter(y_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0, label='clumpparticles')
    ax2.scatter(y_unb, z_unb, s=0.1, color='blue', alpha=0.5, marker=",", lw=0, label='particles unbound from substructure')
    ax2.set_title("y-z plane", family='serif')
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP)#,scatteryoffsets=[5,5,5,5])
    for l in range(2): #range 3: exactly as many as there are labelled plots!
        lgnd2.legendHandles[l]._sizes = [20]

#####################################
#####################################
# X-Z PLANE

# clumpfinder data

#particle and clumpfinder data
    ax3.scatter(x_part, z_part, s=0.1, color='red', alpha=0.5, marker=",", lw=0, label='clumpparticles')
    ax3.scatter(x_unb, z_unb, s=0.1, color='blue', alpha=0.5, marker=",", lw=0, label='particles unbound from substructure')
    ax3.set_title("x-z plane", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')
    lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP)#,scatteryoffsets=[5,5,5,5])
    for l in range(2): #range 3: exactly as many as there are labelled plots!
        lgnd3.legendHandles[l]._sizes = [20]


    
    fig.tight_layout()
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"
