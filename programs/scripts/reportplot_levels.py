#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# Makes a 3D scatterplot of a halo and the children by levels
# 
from os import getcwd
from sys import argv #command line arguments
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from mpl_toolkits.mplot3d import Axes3D

import unbinding_module as m
import report_module as r

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "halo_levels_"+str(halo)

fontP=FontProperties()
fontP.set_size('x-large')



if __name__ == "__main__":

    # get data
    children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)

    

    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,11))
    ax1 = fig.add_subplot(111, projection='3d')
    

    #setting colorbar
    fullcolorlist=m.fullcolorlist



    # SET PLOT PARAMETERS
    if (len(halox)>10000):
        pointsize=0.1
        pointalpha=0.3
    else:
        pointsize=1
        pointalpha=0.7


    # PLOT CHILDREN
    maxlevel=0
    if (len(children)>0):
        maxlevel=max(child_levels)
        for ilevel in range(0,maxlevel+1):
            x,y,z=m.get_level_particles(child_levels,children,ilevel,x_part,y_part,z_part,clumpid)                
            if x is not None:
                r.plot_3D(x,y,z,ax1,'levels',ilevel+1,-1)

       
    # PLOT HALOS
    r.plot_3D(halox,haloy,haloz,ax1,'halo',0,halo) 

   
    # TWEAK PLOT
    r.tweak_plot_3D(fig,plt,ax1,'levels')
    print "Figure created"
    
    
    
     # saving figure
    this_name=outputfilename
    r.save_fig(this_name,fig,workdir)
    
    plt.close()
