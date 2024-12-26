#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script plots the center of mass of clumps which are not
# halo namegivers and the radius of the particle furthest away.
from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend

outputfilename = "CoM-max_distance-plot"
title='Non-namegivers CoM and maximal particle distance'
workdir= str(getcwd())

noutput=int(argv[1])


def get_particle_data():
    print "Reading in particle data"
    
    for i in range(0,noutput):
        inputfile=str(argv[i+2]) 
        # print "Reading from", inputfile
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2])
        if (i == 0):
            data = temp_data
        else:
            data = np.concatenate((data, temp_data), axis=0)

        temp_clumpid=np.loadtxt(inputfile, dtype='int', skiprows=1,usecols=[6])
        if (i==0):
            clumpid=temp_clumpid
        else:
            clumpid=np.concatenate((clumpid,temp_clumpid), axis=0)

    return data[:,0], data[:,1], data[:,2], clumpid





def get_COM_data():
    print "Reading in CoM data"
    inputfile=str(argv[2+noutput])
    data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[1,2,3,4,5,6,7])
    clumpid=np.loadtxt(inputfile,dtype='int', skiprows=1, usecols=[0]) 
    return clumpid, data[:,0], data[:,1], data[:,2], data[:,3], data[:,4], data[:,5], data[:,6]












########################################################################
########################################################################
########################################################################
########################################################################









if __name__ == "__main__":

    
    
    
    # EXTRACT DATA
    # Extract particle data
    xp, yp, zp, idp = get_particle_data() 
    clumpid, comxph, comyph, comzph, comxp, comyp, comzp, max_dist = get_COM_data()

    # plot
    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(16,6))
    fig.suptitle(title, family='serif', size=10) 
    ax1 = fig.add_subplot(131, aspect='equal', clip_on=True)
    ax2 = fig.add_subplot(132, aspect='equal')
    ax3 = fig.add_subplot(133, aspect='equal')

    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)   


    #setting up an empty scatterplot for pixel reference
    xedges=[0.000, 1.000]
    yedges=[0.000, 1.000]
    emptyscatter=ax1.scatter(xedges, yedges, s=0.0, label='_nolegend_')
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
 

    # Calculating the ratio of pixel-to-unit
    upright = ax1.transData.transform((1.0, 1.0))
    lowleft = ax1.transData.transform((0.0,0.0))
    x_to_pix_ratio = upright[0] - lowleft[0]
    y_to_pix_ratio = upright[1] - lowleft[1]
    # Take the mean value of the ratios because why not 
    #dist_to_pix_ratio = (x_to_pix_ratio + y_to_pix_ratio) / 2.0
    dist_to_pix_ratio = x_to_pix_ratio



    # filter particles
    print "Filtering particles"
    filteredxp=[]
    filteredyp=[]
    filteredzp=[]
    for i in range(0,len(clumpid)):
        this_id=clumpid[i]
        for j in range(0,len(idp)):
            if (idp[j]==this_id):
                filteredxp.append(xp[j])
                filteredyp.append(yp[j])
                filteredzp.append(zp[j])

    # Calculate marker size
    clumpsize = np.zeros(len(max_dist))
    for i in range(0, len(max_dist)):
        calc = np.pi*(max_dist[i]*dist_to_pix_ratio)**2
        clumpsize[i] = calc
        

    fontP=FontProperties()
    fontP.set_size('x-small')

    # Plot it
    ax1.scatter(comxp,comyp,s=clumpsize,alpha=0.2,lw=0,color='b', label='Max dist')
    ax1.scatter(filteredxp, filteredyp, s=0.1, alpha=0.6, lw=0, color='r', label='particles')
    ax1.scatter(comxph,comyph,s=0.5,alpha=1,lw=0,color='g', label='CoM phew')
    ax1.scatter(comxp,comyp,s=0.5,alpha=1,lw=0,color='k', label='CoM part')
    ax1.set_title("xy - plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP,scatteryoffsets=[5,5,5,5])
    for l in range(4):
        lgnd1.legendHandles[l]._sizes = [0.3]
    
    
    
    ax2.scatter(comyp,comzp,s=clumpsize,alpha=0.2,lw=0,color='b', label='Max dist')
    ax2.scatter(filteredyp, filteredzp, s=0.1, alpha=0.6, lw=0, color='r', label='particles')
    ax2.scatter(comyp,comzp,s=0.5,alpha=1,lw=0,color='k', label='CoM part')
    ax2.scatter(comyph,comzph,s=0.5,alpha=1,lw=0,color='g', label='CoM phew')
    ax2.set_title("yz - plane", family='serif')
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    ax2.set_xlim(0.00,1.00)
    ax2.set_ylim(0.00,1.00)   
    lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP,scatteryoffsets=[5,5,5,5])
    for l in range(4):
        lgnd2.legendHandles[l]._sizes = [0.3]
    
    
    ax3.scatter(comxp,comzp,s=clumpsize,alpha=0.2,lw=0,color='b', label='Max dist')
    ax3.scatter(filteredxp, filteredzp, s=0.1, alpha=0.6, lw=0, color='r', label='particles')
    ax3.scatter(comxp,comzp,s=0.5,alpha=1,lw=0,color='k', label='CoM part')
    ax3.scatter(comxph,comzph,s=0.5,alpha=1,lw=0,color='g', label='CoM phew')
    ax3.set_title("xz - plane", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')
    ax3.set_xlim(0.00,1.00)
    ax3.set_ylim(0.00,1.00)   
    lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP,scatteryoffsets=[5,5,5,5])
    for l in range(4):
        lgnd3.legendHandles[l]._sizes = [0.3]

        

    print "Figure created"
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"
       
