#!/usr/bin/python

# Creates a 3D scatterplot of subhalo particles of dice sub run
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

outputfilename = "dice-sub-plot-subclumps"




if __name__ == "__main__":

    # get data
    children,child_levels,clumpx,clumpy,clumpz = r.get_clump_data(halo,noutput)
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = r.get_particle_data(children,halo,noutput,particles)

    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,11))
    ax1 = fig.add_subplot(111, projection='3d')
    

    #setting colorbar
    fullcolorlist=r.fullcolorlist

    # PLOT HALOS
    # r.plot_3D(halox,haloy,haloz,ax1,'halo-sub',0,halo) 

    # PLOT CHILDREN
    x,y,z=r.get_child_particles(x_part,y_part,z_part,clumpid,21555)
    r.plot_3D(x,y,z,ax1,'sub-sub',4,21555)

    childcounter = 0
    for i,child in enumerate(children):
        if child  not in [21537, 14913, 21555]:
            childcounter += 1
            x,y,z=r.get_child_particles(x_part,y_part,z_part,clumpid,child)
            r.plot_3D(x,y,z,ax1,'sub-subsub',childcounter,children[i])

    # TWEAK PLOT
    r.tweak_plot_3D(fig,plt,ax1,'sub-sub')
    print "Figure created"
    
    
    # saving figure
    this_name=outputfilename
    r.save_fig(this_name,fig,workdir)

    plt.close()
