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

outputfilename = "plot_"+str(halo)+"-halo-border-circles-after-unbinding"

fontP=FontProperties()
fontP.set_size('xx-small') 

def get_COM(children,plot_child):

    print "Reading in CoM data"
    if (len(children)>0):
        comx=np.zeros(len(children))
        comz=np.zeros(len(children))
        comy=np.zeros(len(children))

        for i in range(0,noutput):
            inputfile=str(argv[i+4+2*noutput]) 
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3])
            if(temp_data.shape[0]>0):
                if 'data' in locals():
                    data = np.vstack((data, temp_data))
                else:
                    data = temp_data


        if (len(data.shape)>1):
            for j in range(0,data.shape[0]):
                for i in range(0,len(children)):
                    if(data[j,0]==children[i]):
                        if (plot_child[i]):
                            comx[i]=(data[j,1])
                            comy[i]=(data[j,2])
                            comz[i]=(data[j,3])
        else:
            for i in range(0,len(children)):
                if(data[0]==children[i]):
                    comx[i]=(data[j,1])
                    comy[i]=(data[j,2])
                    comz[i]=(data[j,3])

            
    else:
        comx=[]
        comy=[]
        comz=[]
    return comx, comy, comz



def get_closest_border(children,plot_child):

    print "Reading in border data"
    if (len(children)>0):
        bx=np.zeros(len(children))
        by=np.zeros(len(children))
        bz=np.zeros(len(children))

        for i in range(0,noutput):
            inputfile=str(argv[i+4+3*noutput]) 
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3])
            if(temp_data.shape[0]>0):
                if 'data' in locals():
                    data = np.vstack((data, temp_data))
                else:
                    data = temp_data


        if (len(data.shape)>1):
            for j in range(0,data.shape[0]):
                for i in range(0,len(children)):
                    if(data[j,0]==children[i]):
                        if (plot_child[i]):
                            bx[i]=(data[j,1])
                            by[i]=(data[j,2])
                            bz[i]=(data[j,3])
        else:
            for i in range(0,len(children)):
                if(data[0]==children[i]):
                    bx[i]=(data[j,1])
                    by[i]=(data[j,2])
                    bz[i]=(data[j,3])

            
    else:
        bx=[]
        by=[]
        bz=[]
    
    return bx, by, bz




if __name__ == "__main__":

    # get data
    children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo,noutput)
    x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)


    #setting colorbar
    fullcolorlist=m.fullcolorlist

    #Optional: get which children should be plottet/filter children
    toomanychildren=(len(children)>len(fullcolorlist))
    if (len(children)>0):
        if (toomanychildren):
            print "Too many children for colorlist ("+str(len(children))+"). Aborting."
            exit()
            print children
        else:
            plot_child=[]
            for i in range(0, len(children)):
                plot_child.append(m.is_child_interesting(clumpid,children[i]))


    comx, comy, comz = get_COM(children,plot_child)
    bx,by,bz=get_closest_border(children,plot_child) 
    N=len(children)


    print "Creating figure"

    plt.close('all')
    # creating empty figure with 3 subplots
    fig = plt.figure(facecolor='white', figsize=(24,9),dpi=450)
    fig.suptitle('plot closest border', family='serif', size=20)

    ax1 = fig.add_subplot(131,aspect='equal')
    ax2 = fig.add_subplot(132,aspect='equal')
    ax3 = fig.add_subplot(133,aspect='equal')


    offset=0.1
    xmin=clumpx-offset
    ymin=clumpy-offset
    zmin=clumpz-offset
    xmax=clumpx+offset
    ymax=clumpy+offset
    zmax=clumpz+offset

    ax1.set_xlim(xmin,xmax)
    ax1.set_ylim(ymin,ymax)   
    ax2.set_xlim(ymin,ymax)   
    ax2.set_ylim(zmin,zmax)   
    ax3.set_xlim(xmin,xmax)
    ax3.set_ylim(zmin,zmax)   

    print "lencomp", len(children), len(comx), len(bx), len(plot_child)

    for i in range(len(children)):
        print i,children[i], comx[i], comy[i], comz[i], bx[i], by[i], bz[i], plot_child[i]
        if plot_child[i]:
            # Plot circles
            dist=[np.sqrt( (comx[i]-bx[i])**2+(comy[i]-by[i])**2+(comz[i]-bz[i])**2 )]
            scat1=ax1.scatter(comx[i],comy[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
            scat2=ax2.scatter(comy[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
            scat3=ax3.scatter(comx[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
           
            fig.canvas.draw()
            # Calculate radius in pixels :
            rr_pix1 = (ax1.transData.transform(np.vstack([dist, dist]).T) - ax1.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
            rpix1, _ = rr_pix1.T

            rr_pix2 = (ax2.transData.transform(np.vstack([dist, dist]).T) - ax2.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
            rpix2, _ = rr_pix2.T
            
            rr_pix3 = (ax3.transData.transform(np.vstack([dist, dist]).T) - ax3.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
            rpix3, _ = rr_pix3.T

            # Calculate and update size in points:
            size_pt1 = (2*rpix1/fig.dpi*72)**2
            size_pt2 = (2*rpix2/fig.dpi*72)**2
            size_pt3 = (2*rpix3/fig.dpi*72)**2
            scat1.set_sizes(size_pt1)
            scat2.set_sizes(size_pt2)
            scat3.set_sizes(size_pt3)




    # SET PLOT PARAMETERS
    if (len(halox)>10000):
        pointsize=0.1
        pointalpha=0.3
    else:
        pointsize=1
        pointalpha=0.7



     # PLOT HALOS
    m.plot_2D(halox,haloy,haloz,ax1,ax2,ax3,pointsize,pointalpha,'halo',0,halo) 

   
    # PLOT CHILDREN
    if (len(children)>0):
        if (toomanychildren):
            for ilevel in range(0,maxlevel+1):
                x,y,z=m.get_level_particles(child_levels,children,ilevel,x_part,y_part,z_part,clumpid)                
                if x is not None:
                    m.plot_2D(x,y,z,ax1,ax2,ax3,pointsize,pointalpha,'levels',ilevel+1,-1)
        else:
            for i in range(0, len(children)):
                if plot_child[i]:
                    x,y,z=m.get_child_particles(x_part,y_part,z_part,clumpid,children[i])
                    m.plot_2D(x,y,z,ax1,ax2,ax3,pointsize,pointalpha,'children',i+1,children[i])

    for i in range(len(children)):
        if plot_child[i]:
            #HERE
            # PLOT COMs
            m.plot_2D(comx[i],comy[i],comz[i],ax1,ax2,ax3,pointsize,1.0,'COM',i+1,children[i])
            # Plot borders 
            m.plot_2D(bx[i],by[i],bz[i],ax1,ax2,ax3,pointsize,1.0,'border',i+1,children[i])
                
    # TWEAK PLOT
    # fig.canvas.draw()
    ax1.set_title("x-y plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax2.set_title("y-z plane", family='serif')
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    ax3.set_title("x-z plane", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')
    print "Figure created"

    # SET LEGEND
    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    unbc=0
   
   
    for l in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[l]._sizes = [20]
        lgnd2.legendHandles[l]._sizes = [20]
        lgnd3.legendHandles[l]._sizes = [20]
   
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False,dpi=450)
    plt.close()

    print "done", outputfilename+".png"
