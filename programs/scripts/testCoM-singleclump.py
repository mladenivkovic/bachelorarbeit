#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script plots the center of mass of clumps which are not
# halo namegivers and the radius of the particle furthest away.
# It creates a plot for each clump separately in the subdirectory
# CoM-output.

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






def create_plot(k):

    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white',figsize=(5,5))# figsize=(10,32))
    fig.suptitle(title, family='serif', size=10) 
    ax1 = fig.add_subplot(111, aspect='equal', clip_on=True)
    ax1.set_xbound(lower=0.0,upper=1.0)
    # ax2 = fig.add_subplot(312, aspect='equal')
    # ax3 = fig.add_subplot(313, aspect='equal')

    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
#     ax2.set_xlim(0.00,1.00)
    # ax2.set_ylim(0.00,1.00)   
    # ax3.set_xlim(0.00,1.00)
    # ax3.set_ylim(0.00,1.00)   


    #setting up an empty scatterplot for pixel reference
    xedges=[0.000, 1.000]
    yedges=[0.000, 1.000]
    emptyscatter=ax1.scatter(xedges, yedges, s=0.0, label='_nolegend_')
    # emptyscatter2=ax2.scatter(xedges, yedges, s=0.0)
    # emptyscatter3=ax3.scatter(xedges, yedges, s=0.0)
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
#     ax2.set_xlim(0.00,1.00)
    # ax2.set_ylim(0.00,1.00)   
    # ax3.set_xlim(0.00,1.00)
    # ax3.set_ylim(0.00,1.00)      
# 

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
#         print max_dist
    # print len(max_dist)
    # print comzp
    # print len(comzp)
    # for i in range(0,len(clumpid)):
    this_id=clumpid[k]
    for j in range(0,len(idp)):
        if (idp[j]==this_id):
            filteredxp.append(xp[j])
            filteredyp.append(yp[j])
            filteredzp.append(zp[j])

    # Calculate radius
    # Calculate marker size
    # clumpsize = np.zeros(len(max_dist))
    # for i in range(0, len(max_dist)):
    #     calc = (max_dist[i]*dist_to_pix_ratio)**2
        # clumpsize[i] = calc
        
    clumpsize=np.pi*max_dist[k]**2*dist_to_pix_ratio**2


    fontP=FontProperties()
    fontP.set_size('x-small')

    # Plot it
    ax1.scatter(comxp[k],comyp[k],s=clumpsize,alpha=0.2,lw=0,color='b', label='Max dist')
    ax1.scatter(filteredxp, filteredyp, s=0.1, alpha=0.6, lw=0, color='r', label='particles')
    ax1.scatter(comxp[k],comyp[k],s=1,alpha=1,lw=0,color='k', label='CoM p')
    ax1.scatter(comxph[k],comyph[k],s=1,alpha=1,lw=0,color='g', label='CoM phew')
    ax1.set_title("xy - plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_xlim(0.00,1.00)
    ax1.set_ylim(0.00,1.00)   
    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP,scatteryoffsets=[5,5,5,5])
    for l in range(4):
        lgnd1.legendHandles[l]._sizes = [0.3]

    # lgnd1.legendHandles[1]._sizes = [1]





        

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/CoM-output/'+outputfilename+str(this_id)+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "done", outputfilename+".png"














########################################################################
########################################################################
########################################################################
########################################################################









if __name__ == "__main__":

    
    
    
    #################################
    # EXTRACT DATA
    # Extract particle data
    xp, yp, zp, idp = get_particle_data() 
    clumpid, comxph, comyph, comzph, comxp, comyp, comzp, max_dist = get_COM_data()

    # plot
    # for k in range(len(clumpid)):
    for k in range(0,len(clumpid)):
        create_plot(k)
        
