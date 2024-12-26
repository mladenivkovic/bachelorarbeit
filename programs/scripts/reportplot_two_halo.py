#!/usr/bin/python

# Plots only particles belonging to defined halo. 
# 
from os import getcwd
from sys import argv #command line arguments
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from mpl_toolkits.mplot3d import Axes3D

import report_module as m

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "dice-two-halo-only"


if __name__ == "__main__":

    # get data
    # children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    children=[]  
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)


    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,11))
    ax1 = fig.add_subplot(111, projection='3d')
    
    fullcolorlist=m.fullcolorlist

    pointsize=1
    mylw=0.0
    mymarker=','
    pointalpha=0.2

    counter=0
    halolabel=r'halo-namegiver particles'
    ax1.scatter(halox,haloy,haloz,s=pointsize,c=fullcolorlist[counter], label=halolabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)

     
    m.tweak_plot_3D(fig,plt, ax1,'two')
  
       
    this_name=outputfilename
    m.save_fig(this_name,fig,workdir)

    plt.close()
