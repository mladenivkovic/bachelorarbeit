#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script plots all particles that are in clumps and mark the ones 
# that were unbound. It makes 3 subplots,
# one for each plane of coordinates: xy, yz and xz
# 
from os import getcwd
from sys import argv,exit #command line arguments
import matplotlib 
# matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

import unbinding_module as m

workdir= str(getcwd())

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

outputfilename = "plot_"+str(halo)+"-border"

fontP=FontProperties()
fontP.set_size('xx-small') 

def get_COM(children):
    print "Reading in CoM data"
    if (len(children)>0):
        for i in range(0,noutput):
            inputfile=str(argv[i+4+2*noutput]) 
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3])
            if(temp_data.shape[0]>0):
                if 'data' in locals():
                    data = np.vstack((data, temp_data))
                else:
                    data = temp_data
        comx=[]
        comy=[]
        comz=[]
        print data 
        if (len(data.shape)>1):
            for j in range(0,data.shape[0]):
                for i in range(0,len(children)):
                    if(data[j,0]==children[i]):
                        comx.append(data[j,1])
                        comy.append(data[j,2])
                        comz.append(data[j,3])
        else:
            for i in range(0,len(children)):
                if(data[0]==children[i]):
                    comx.append(data[1])
                    comy.append(data[2])
                    comz.append(data[3])

            
    else:
        comx=[]
        comy=[]
        comz=[]
    return comx, comy, comz



def get_closest_border(children):
    print "Reading in border data"
    if (len(children)>0):
        for i in range(0,noutput):
            inputfile=str(argv[i+4+3*noutput]) 
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3])
            if(temp_data.shape[0]>0):
                if 'data' in locals():
                    data = np.vstack((data, temp_data))
                else:
                    data = temp_data
        bx=[]
        by=[]
        bz=[]
        print data 
        if (len(data.shape)>1):
            for j in range(0,data.shape[0]):
                for i in range(0,len(children)):
                    if(data[j,0]==children[i]):
                        bx.append(data[j,1])
                        by.append(data[j,2])
                        bz.append(data[j,3])
        else:
            for i in range(0,len(children)):
                if(data[0]==children[i]):
                    bx.append(data[1])
                    by.append(data[2])
                    bz.append(data[3])

            
    else:
        bx=[]
        by=[]
        bz=[]
    return bx, by, bz




if __name__ == "__main__":

    # get data
    children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)
    comx, comy, comz = get_COM(children)
    bx,by,bz=get_closest_border(children) 

    print "Creating figure"

    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(24,12))
    fig.suptitle('plot closest border', family='serif', size=20)

    ax1 = fig.add_subplot(131)
    ax2 = fig.add_subplot(132)
    ax3 = fig.add_subplot(133)

    #setting colorbar
    fullcolorlist=m.fullcolorlist

    toomanychildren=(len(children)>len(fullcolorlist))


    # SET PLOT PARAMETERS
    if (len(halox)>10000):
        pointsize=0.1
        pointalpha=0.3
    else:
        pointsize=1
        pointalpha=0.7

    if (len(x_part)<2000000):
        if (len(children)>0):
            m.make_fancy_axes(ax1,ax2,ax3,1,clumpx,clumpy,clumpz,x_part, y_part,z_part,True)
        else:
            m.make_fancy_axes(ax1,ax2,ax3,1,clumpx,clumpy,clumpz,halox,haloy,haloz,True)


     # PLOT HALOS
    # m.plot_2D(halox,haloy,haloz,ax1,ax2,ax3,pointsize,pointalpha,'halo',0,halo) 

   
    # PLOT CHILDREN
    maxlevel=0
    if (len(children)>0):
        if (toomanychildren):
            print "Too many children for colorlist ("+str(len(children))+"). Aborting."
            exit()
            print children

            maxlevel=max(child_levels)
            for ilevel in range(0,maxlevel+1):
                x,y,z=m.get_level_particles(child_levels,children,ilevel,x_part,y_part,z_part,clumpid)                
                if x is not None:
                    m.plot_2D(x,y,z,ax1,ax2,ax3,pointsize,pointalpha,'levels',ilevel+1,-1)

        else:
            plot_child=[]
            for i in range(0, len(children)):
                x,y,z=m.get_child_particles(x_part,y_part,z_part,clumpid,children[i])
                # if len(x)>10:
                plot_child.append(True)
                m.plot_2D(x,y,z,ax1,ax2,ax3,pointsize,pointalpha,'children',i+1,children[i])
                # else:
                #     plot_child.append(False)

    # PLOT UNBOUND PARTICLES
   #  if (len(unboundx)>0): 
        # if (toomanychildren):
        #     for ilevel in range(0,maxlevel+1):
                # xu=None
   #              yu=None
        #         zu=None
        #         print "Plotting unbound particles for level "+str(ilevel)
        #         xu,yu,zu=m.get_level_particles(child_levels,children,ilevel,unboundx,unboundy,unboundz,uclid)                
        #         if xu is not None:
        #             m.plot_2D(xu,yu,zu,ax1,ax2,ax3,pointsize,pointalpha,'unblev',ilevel,-1)
        #         else:
        #             print "Found no unbound  particles belonging to substructure at this level."
        # 
        #         xu,yu,zu=m.get_level_particles([0],[halo],ilevel,unboundx,unboundy,unboundz,uclid)
        #         if xu is not None:
        #             m.plot_2D(xu,yu,zu,ax1,ax2,ax3,pointsize,pointalpha,'unblev',ilevel,-1)
        #         else:
        #             if (ilevel==0):
        #                 print "Found no unbound particles belonging to the halo."
        # 
        # else: # not toomanychildren
            # for i in range(len(children)):
    #             xu=None
            #     yu=None
            #     zu=None
            #     xu,yu,zu=m.get_child_particles(unboundx,unboundy,unboundz,uclid,children[i])
            #     if len(xu)>0:
            #         m.plot_2D(xu,yu,zu,ax1,ax2,ax3,pointsize,pointalpha,'unbound',i+1,children[i])
            #     else:
            #         print "Found no unbound particle assigned to child "+str(children[i])
            # xu=None
            # yu=None
            # zu=None
            # xu,yu,zu=m.get_child_particles(unboundx,unboundy,unboundz,uclid,halo)
            # if len(xu)>0:
            #     m.plot_2D(xu,yu,zu,ax1,ax2,ax3,pointsize,pointalpha,'unbound',0,halo)
            # else:
            #     print "Found no unbound particles for halo-namegiver "+str(halo)
            # 
        # print len(data.shape)
    # else:
        # print "No unbound particles found."
        # plt.figtext(.05, .03, 'No unbound particles.', family='serif', size=10)


    # PLOT COMs
    for i in range(len(children)):
        if plot_child[i]:
            m.plot_2D(comx[i],comy[i],comz[i],ax1,ax2,ax3,pointsize,1.0,'COM',i+1,children[i])
        
            m.plot_2D(bx[i],by[i],bz[i],ax1,ax2,ax3,pointsize,1.0,'border',i+1,children[i])
    
    # TWEAK PLOT
    m.tweak_plot_2D(fig,ax1,ax2,ax3,fontP)
    print "Figure created"
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=450)
    plt.close()

    print "done", outputfilename+".png"
