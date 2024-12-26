#!/usr/bin/python

    # creates image for cosmo runs: whole domain, clumpparticles by levels
# 
from os import getcwd
from sys import argv #command line arguments
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from mpl_toolkits.mplot3d import Axes3D

import report_module as r

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "cos_plot"




if __name__ == "__main__":

    # # get data

    # halos,maxlevel,children,child_levels=r.get_halo_list(noutput)
    levels,maxlevel=r.get_level_list(noutput)
    x,y,z,halox,haloy,haloz=r.get_particle_data_level(levels,noutput,particles,maxlevel)
    
    print "Creating figure"
    
    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,10))
    ax1 = fig.add_subplot(111, aspect='equal')
    # ax1 = fig.add_subplot(111, aspect='equal',projection='3d')
    
    
    #setting colorbar
    fullcolorlist=r.fullcolorlist
    print halox, haloy, haloz 
    # PLOT HALOS
    r.plot_2D(halox,haloy,ax1,'halo-cos',0) 
    # r.plot_3D(halox,haloy,haloz,ax1,'halo-cos',0,0) 
    
    # PLOT CHILDREN
    for level in range(0, maxlevel+1):
        r.plot_2D(x[level],y[level],ax1,'sub-cos',level+1)
        
    # TWEAK PLOT
    r.tweak_plot_2D(fig,plt,ax1,'cos')
    print "Figure created"

    # saving figure
    this_name=outputfilename
    r.save_fig(this_name,fig,workdir)
    
    plt.close()
