#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

from os import getcwd
from sys import argv,exit #command line arguments
import matplotlib 
import warnings
# matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size

import unbinding_module as m

workdir= str(getcwd())

noutput=int(argv[1])
particles=int(argv[2])


fontP=FontProperties()
fontP.set_size('xx-small') 


#setting colorbar
fullcolorlist=m.fullcolorlist


def get_COM(children,plot_child):

    print "Reading in CoM data"
    if (len(children)>0):
        comx=np.zeros(len(children))
        comz=np.zeros(len(children))
        comy=np.zeros(len(children))

        for i in range(0,noutput):
            inputfile=str(argv[i+3+2*noutput]) 
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
            inputfile=str(argv[i+3+3*noutput]) 
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



def get_all_particles(noutput,particles):
    print "Reading in particle data"
    data=np.zeros((particles,5))
    particle_index=0
    for i in range(0,noutput):
        inputfile=str(argv[i+3+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6,7])
    
        if (temp_data.shape[0]>0):
            for j in range(temp_data.shape[0]):
                for k in range(5):
                    data[j+particle_index,k]=temp_data[j,k]
        
            particle_index=particle_index+temp_data.shape[0]-1

    # filter out all non-clump particles
    filteredx=np.zeros(particles) #first guess for length.
    filteredy=np.zeros(particles)
    filteredz=np.zeros(particles)
    clumpid=np.zeros(particles)

    fc=0

    for i in range(data.shape[0]):
        if (data[i,3]>0):
            filteredx[fc]=data[i,0]  
            filteredy[fc]=data[i,1]
            filteredz[fc]=data[i,2] 
            clumpid[fc]=data[i,3]
            fc+=1


    fx=np.zeros(fc)
    fy=np.zeros(fc)
    fz=np.zeros(fc)
    cid=np.zeros(fc)
    for i in range(fc):
        fx[i]=filteredx[i]
        fy[i]=filteredy[i]
        fz[i]=filteredz[i]
        cid[i]=clumpid[i]

    return fx, fy, fz, cid









def get_all_clump_data(noutput):

    print "Reading in clump data"

    for i in range(0,noutput):
        inputfile=str(argv[i+3]) 
        
        # get clump center
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[4,5,6])
        if(temp_data.shape[0]>0):
            if 'data' in locals():
                data = np.vstack((data, temp_data))
            else:
                data = temp_data
        

        #get clump ids, parents and levels
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0,1,2])
        if(temp_data_int.shape[0]>0):
            if 'data_int' in locals():
                data_int= np.vstack((data_int, temp_data_int))
            else:
                data_int = temp_data_int


    allclumpx=data[:,0]
    allclumpy=data[:,1]
    allclumpz=data[:,2]
    allclumpid=data_int[:,0]
    allclumplvl=data_int[:,1]
    parent=data_int[:,2]



    return allclumpx, allclumpy, allclumpz, allclumpid, allclumplvl, parent















def get_clump_data(halo,parent,allclumplvl,allclumpx,allclumpy,allclumpz,clumpid):


    children=[]
    child_levels=[]

    i=0
    while(i<len(parent)):
        if (parent[i] in children or parent[i]==halo): #if parent is halo or one of the children
            if (clumpid[i] != halo):
                if (children.count(clumpid[i])==0):
                    children.append(clumpid[i])
                    child_levels.append(allclumplvl[i])
                    i=-1
            else:
                clumpx=allclumpx[i]
                clumpy=allclumpy[i]
                clumpz=allclumpz[i]

        i+=1





    return children, child_levels, clumpx, clumpy, clumpz




    
    
def get_halo_particles(x_part,y_part,z_part,clumpid,halo):
    xtemp=np.zeros(len(x_part))
    ytemp=np.zeros(len(x_part))
    ztemp=np.zeros(len(x_part))
    counter=0
    for j in range(0,len(x_part)):
        if (clumpid[j]==halo):
            xtemp[counter]=x_part[j]
            ytemp[counter]=y_part[j]
            ztemp[counter]=z_part[j]
            counter+=1

    x=np.zeros(counter)
    y=np.zeros(counter)
    z=np.zeros(counter)
    for j in range(counter):
        x[j]=xtemp[j]
        y[j]=ytemp[j]
        z[j]=ztemp[j]
    
    ##########################################
    # print out particles if needed
    #         for j in range(len(x)):
    #             print ('{0:12.7f}{1:12.7f}{2:12.7f}{3:12d}'.format(x[j], y[j], z[j], i+1))
    ##########################################

    return x, y, z








def plotloop(halo,allclumpx,allclumpy,allclumpz,allclumpid,allclumplvl,parent,xpart,ypart,zpart,pclid):

    print "working on halo", halo
    outputfilename = "plot_"+str(halo)+"_borderCircles"



    children,child_levels,clumpx,clumpy,clumpz = get_clump_data(halo,parent,allclumplvl,allclumpx,allclumpy,allclumpz,allclumpid)
    
    halox,haloy,haloz=get_halo_particles(xpart,ypart,zpart,pclid,halo)

    toomanychildren=(len(children)>len(fullcolorlist))
    if (len(children)>0):
        if (toomanychildren):
            print "Too many children for colorlist ("+str(len(children))+"). Aborting."
            exit()
            print children
        else:
            plot_child=[]
            for i in range(0, len(children)):
                plot_child.append(m.is_child_interesting(pclid,children[i]))


    comx, comy, comz = get_COM(children,plot_child)
    bx,by,bz=get_closest_border(children,plot_child) 
    N=len(children)


    to_plot = False
    for i in plot_child:
        to_plot=to_plot or i
        if to_plot:
            break

    print to_plot
    print plot_child 

    if(to_plot):
        print "Creating figure"

        plt.close('all')
        # creating empty figure with 3 subplots
        fig = plt.figure(facecolor='white', figsize=(24,18),dpi=450)
        fig.suptitle('plot closest border', family='serif', size=20)

        ax1 = fig.add_subplot(231,aspect='equal')
        ax2 = fig.add_subplot(232,aspect='equal')
        ax3 = fig.add_subplot(233,aspect='equal')
        ax4 = fig.add_subplot(234,aspect='equal')
        ax5 = fig.add_subplot(235,aspect='equal')
        ax6 = fig.add_subplot(236,aspect='equal')


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
        ax4.set_xlim(xmin,xmax)
        ax4.set_ylim(ymin,ymax)   
        ax5.set_xlim(ymin,ymax)   
        ax5.set_ylim(zmin,zmax)   
        ax6.set_xlim(xmin,xmax)
        ax6.set_ylim(zmin,zmax)   


        for i in range(len(children)):
            # print i,children[i], comx[i], comy[i], comz[i], bx[i], by[i], bz[i], plot_child[i]
            if plot_child[i]:
                # Plot circles
                dist=[np.sqrt( (comx[i]-bx[i])**2+(comy[i]-by[i])**2+(comz[i]-bz[i])**2 )]
                scat1=ax1.scatter(comx[i],comy[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
                scat2=ax2.scatter(comy[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
                scat3=ax3.scatter(comx[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
                scat4=ax4.scatter(comx[i],comy[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
                scat5=ax5.scatter(comy[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
                scat6=ax6.scatter(comx[i],comz[i],s=0,c=fullcolorlist[i+1],alpha=0.2, lw=0.1)
               
                fig.canvas.draw()
                # Calculate radius in pixels :
                rr_pix1 = (ax1.transData.transform(np.vstack([dist, dist]).T) - ax1.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
                rpix1, _ = rr_pix1.T

                rr_pix2 = (ax2.transData.transform(np.vstack([dist, dist]).T) - ax2.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
                rpix2, _ = rr_pix2.T
                
                rr_pix3 = (ax3.transData.transform(np.vstack([dist, dist]).T) - ax3.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))
                rpix3, _ = rr_pix3.T

                rr_pix4 = (ax4.transData.transform(np.vstack([dist, dist]).T) - ax4.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))

                rr_pix5 = (ax5.transData.transform(np.vstack([dist, dist]).T) - ax5.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))

                rr_pix6 = (ax6.transData.transform(np.vstack([dist, dist]).T) - ax6.transData.transform(np.vstack([np.zeros(N), np.zeros(N)]).T))


                # Calculate and update size in points:
                size_pt1 = (2*rpix1/fig.dpi*72)**2
                size_pt2 = (2*rpix2/fig.dpi*72)**2
                size_pt3 = (2*rpix3/fig.dpi*72)**2
                size_pt4 = (2*rpix1/fig.dpi*72)**2
                size_pt5 = (2*rpix2/fig.dpi*72)**2
                size_pt6 = (2*rpix3/fig.dpi*72)**2
                scat1.set_sizes(size_pt1)
                scat2.set_sizes(size_pt2)
                scat3.set_sizes(size_pt3)
                scat4.set_sizes(size_pt4)
                scat5.set_sizes(size_pt5)
                scat6.set_sizes(size_pt6)



        # SET PLOT PARAMETERS
        if (len(halox)>10000):
            pointsize=0.1
            pointalpha=0.3
        else:
            pointsize=1
            pointalpha=0.7



         # PLOT HALOS
        m.plot_2D(halox,haloy,haloz,ax4,ax5,ax6,pointsize,pointalpha,'halo',0,halo) 

       


        # PLOT CHILDREN
        if (len(children)>0):
            for i in range(0, len(children)):
                if plot_child[i]:
                    xi,yi,zi=m.get_child_particles(xpart,ypart,zpart,pclid,children[i])
                    print "plotting", len(x), "particles assigned to child", children
                    m.plot_2D(xi,yi,zi,ax1,ax2,ax3,pointsize,pointalpha,'children',i+1,children[i])
                    m.plot_2D(xi,yi,zi,ax4,ax5,ax6,pointsize,pointalpha,'children',i+1,children[i])

        for i in range(len(children)):
            if plot_child[i]:
                #HERE
                # PLOT COMs
                m.plot_2D(comx[i],comy[i],comz[i],ax1,ax2,ax3,pointsize,1.0,'COM',i+1,children[i])
                m.plot_2D(comx[i],comy[i],comz[i],ax4,ax5,ax6,pointsize,1.0,'COM',i+1,children[i])
                # Plot borders 
                m.plot_2D(bx[i],by[i],bz[i],ax1,ax2,ax3,pointsize,1.0,'border',i+1,children[i])
                m.plot_2D(bx[i],by[i],bz[i],ax4,ax5,ax6,pointsize,1.0,'border',i+1,children[i])



                            
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
        ax4.set_title("x-y plane", family='serif')
        ax4.set_xlabel('x')
        ax4.set_ylabel('y')
        ax5.set_title("y-z plane", family='serif')
        ax5.set_xlabel('y')
        ax5.set_ylabel('z')
        ax6.set_title("x-z plane", family='serif')
        ax6.set_xlabel('x')
        ax6.set_ylabel('z')

        print "Figure created"

        # SET LEGEND
        lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
        lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
        lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
        lgnd4=ax4.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
        lgnd5=ax5.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
        lgnd6=ax6.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
       
       
        for l in range(len(lgnd1.legendHandles)):
            lgnd1.legendHandles[l]._sizes = [20]
            lgnd2.legendHandles[l]._sizes = [20]
            lgnd3.legendHandles[l]._sizes = [20]

        for l in range(len(lgnd4.legendHandles)):
            lgnd4.legendHandles[l]._sizes = [20]
            lgnd5.legendHandles[l]._sizes = [20]
            lgnd6.legendHandles[l]._sizes = [20]
       
        # saving figure
        fig_path = workdir+'/'+outputfilename+'.png'
        print "saving figure as "+fig_path
        plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False,dpi=450)
        plt.close()

        print "done", outputfilename+".png"

    else:

        print "No children for this halo found. Aborting."

    return







def get_halos(allclumpid,parents):
    
    halos=[]

    for i in range(len(allclumpid)):
        if allclumpid[i]==parents[i]:
            halos.append(allclumpid[i])


    return halos








if __name__ == "__main__":

    # get data
    x,y,z,pclid=get_all_particles(noutput,particles)
    allclumpx, allclumpy, allclumpz, allclumpid, allclumplvl, parent=get_all_clump_data(noutput)

    halos=get_halos(allclumpid,parent)
    # halos=[76, 110, 112, 124, 135, 141, 149, 155, 169, 192, 235, 274, 996, 1043, 1066, 1112, 1126, 1179, 1221, 1230, 1272, 1277, 1356, 1441, 1479, 1488, 1605, 1629, 1651, 1712, 1713, 1737, 1741, 1808, 1878, 1968, 2034, 3715, 3749, 3894, 3918, 3934, 4225, 4271, 4381, 4685, 4796, 5087, 5163, 5250, 5413, 5462, 5480, 5519, 5520, 5542, 5549, 5581, 5635, 5638, 5725, 5775, 5799, 6182, 6192, 6244, 6282, 6441, 6486, 6567, 6634, 6670, 6674, 6689, 6800, 6835, 7105, 7122, 7230, 7276, 7313, 7396, 7445, 7490, 7523, 7555, 7638, 7660, 7717, 8045, 8228, 8298, 8364, 8471, 8528, 8619, 8629, 8752, 8758, 8765, 8883, 8890, 8998, 9016, 9061, 9156, 9166, 9197, 9261, 9353, 9444, 9513, 9541, 9609, 9700, 9702, 9741, 10085, 10104, 10205, 10678, 10741, 10756]

    for i in halos:
        plotloop(i,allclumpx,allclumpy,allclumpz,allclumpid,allclumplvl,parent,x,y,z,pclid)
