#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# Plots only particles belonging to defined halo. 
# 
from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from mpl_toolkits.mplot3d import Axes3D

import unbinding_module as m

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "singleclump_plot"+str(halo)+'_3D'

fontP=FontProperties()
fontP.set_size('xx-small') 



if __name__ == "__main__":

    # get data
    # children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    children=[]  
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)


    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,4))
    fig.suptitle('separated clump plot '+str(halo), family='serif', size=20)
    ax1 = fig.add_subplot(141, projection='3d')
    ax2 = fig.add_subplot(142, projection='3d')
    ax3 = fig.add_subplot(143, projection='3d')
    ax4 = fig.add_subplot(144, projection='3d')
    

    #setting colorbar
    fullcolorlist=m.fullcolorlist


    # SET PLOT PARAMETERS
    if (len(halox)>10000):
        pointsize=0.1
        pointalpha=0.3
    else:
        pointsize=1
        pointalpha=0.7

    # if (len(x_part)<500000):
    #     if (len(children)>0):
    #         m.make_fancy_axes(ax1,ax2,ax3,ax4,clumpx,clumpy,clumpz,x_part, y_part,z_part,False)
    #     else:
    #         m.make_fancy_axes(ax1,ax2,ax3,ax4,clumpx,clumpy,clumpz,halox,haloy,haloz,False)
    # 



    # PLOT HALOS
    m.plot_3D(halox,haloy,haloz,ax1,ax2,ax3,ax4,pointsize,pointalpha,'clump',0,halo) 

    #plot unbound particles
    
    if (len(unboundx)>0): 
        xu=None
        yu=None
        zu=None
        xu,yu,zu=m.get_child_particles(unboundx,unboundy,unboundz,uclid,halo)
        if len(xu)>0:
            m.plot_3D(xu,yu,zu,ax1,ax2,ax3,ax4,pointsize,pointalpha,'unbound',0,halo)
        else:
            print "Found no unbound particles for halo-namegiver "+str(halo)

    else:
        print "No unbound particles found."
        plt.figtext(.05, .03, 'No unbound particles.', family='serif', size=10)

 
  
    # TWEAK PLOT
    m.tweak_plot_3D(fig,ax1,ax2,ax3,ax4,fontP)
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"



    
