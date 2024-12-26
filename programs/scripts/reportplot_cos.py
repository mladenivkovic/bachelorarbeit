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

outputfilename = "cos-halo-"+str(halo)

minparticles=10

periodichalos=[66858,75]
plotchildren=[235, 1874, 67048, 68234, 7277, 70888]

if __name__ == "__main__":

    # get data
    children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)


    if halo in periodichalos:
        for i,x in enumerate(halox):
            if x > 0.5:
                halox[i] -= 1

  
    xmin=min(halox)
    ymin=min(haloy)
    zmin=min(haloz)
    xmax=max(halox)
    ymax=max(haloy)
    zmax=max(haloz)

    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(10,11))
    ax1 = fig.add_subplot(111, projection='3d')
    

    #setting colorbar
    fullcolorlist=m.fullcolorlist

    # PLOT HALOS
    r.plot_3D(halox,haloy,haloz,ax1,'halo-cos',0,halo) 

    # PLOT CHILDREN
    colorcounter = 0

    for i in range(len(children)):

        x,y,z=r.get_child_particles(x_part,y_part,z_part,clumpid,children[i])
        

        if children[i] in plotchildren:
            colorcounter += 1

            if len(x)>0:

                for k,xx in enumerate(x):
                    if xx > 0.5:
                        x[k] -= 1

                xmin=min(min(x),xmin)
                ymin=min(min(y),ymin)
                zmin=min(min(z),zmin)
                xmax=max(max(x),xmax)
                ymax=max(max(y),ymax)
                zmax=max(max(z),zmax)

                if len(x) > minparticles:
                    r.plot_3D(x,y,z,ax1,'sub-cos',colorcounter,children[i])
                else:
                    r.plot_3D(x,y,z,ax1,'add-to-halo-cos',0,halo)
       
    # TWEAK PLOT
    ax1.set_xlim3d(xmin,xmax)
    ax1.set_ylim3d(ymin,ymax)
    ax1.set_zlim3d(zmin,zmax)
    r.tweak_plot_3D(fig,plt,ax1,'cos')
    print "Figure created"
    
    
    
     # saving figure
    # for e in range(0,181,20):
    #     for a in range(0,361,20):
    # 
    #         ax1.view_init(elev=e,azim=a)
    #         # ax1.view_init(elev=20,azim=120)
    # 
    #         this_name=outputfilename+"-"+str(e)+"-"+str(a)
    #         # this_name=outputfilename
    #         r.save_fig(this_name,fig,workdir)

    # ax1.view_init(elev=20,azim=120)


    this_name=outputfilename
    r.save_fig(this_name,fig,workdir)

    plt.close()
