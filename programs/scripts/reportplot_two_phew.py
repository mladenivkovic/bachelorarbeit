#!/usr/bin/python

# This script plots all particles that are in clumps and mark the ones 
# that were unbound. It makes 3 subplots,
# one for each plane of coordinates: xy, yz and xz
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

outputfilename = "dice-two-plot-halo"+str(halo)




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
    r.plot_3D(halox,haloy,haloz,ax1,'halo-two-phew',0,halo) 

    # PLOT CHILDREN
    if (len(children)>0):
        for i in range(0, len(children)):
            x,y,z=r.get_child_particles(x_part,y_part,z_part,clumpid,children[i])
            r.plot_3D(x,y,z,ax1,'sub',i+1,children[i])

    # TWEAK PLOT
    r.tweak_plot_3D(fig,plt,ax1,'two')
    print "Figure created"
    
    
    # saving figure
    this_name=outputfilename
    r.save_fig(this_name,fig,workdir)

    plt.close()
