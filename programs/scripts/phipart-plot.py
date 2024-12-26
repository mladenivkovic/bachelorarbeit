#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import warnings as warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend

nphi=int(argv[1])
noutput=int(argv[2])
clumpid=int(argv[3])
workdir= str(getcwd())
pot=workdir[-15:]
binning=pot[-7:]
pot=pot[:7]
outputfilename = "partpotential_plot"+str(clumpid)
title=pot+' potential '+binning+' binning for clump '+str(clumpid)
print pot, binning



#Legend stuff
fontP=FontProperties()
fontP.set_size('x-small') # sizes = ['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']

def get_phi(filename):
    print ''
    print " Extracting data from", filename

    data=np.loadtxt(filename, dtype='float', skiprows=1)


    # Other useful options:
    #   skiprows=N   skips first N rows
    #   Each row in the text file must have the same number of values.
    return data[:,0], data[:,1]



def get_particles(counter, clumpid):
    # READ CLUMP DATA IN FIRST
    beforefile=str(argv[counter+4+nphi])
    afterfile=str(argv[counter+4+nphi+noutput])
    print "Reading in particle data"
    x=[]
    y=[]
    z=[]
    vx=[]
    vy=[]
    vz=[]
    ind=[]

    data=np.loadtxt(beforefile, dtype='float', skiprows=1, usecols=[0,1,2,3,4,5,6])
    clmp=np.loadtxt(beforefile,dtype='int',skiprows=1,usecols=[6])
    # clmp=np.loadtxt(beforefile,dtype='int',skiprows=1,usecols=[9])
    
    counter=0
    for i in range(data.shape[0]):
        # if clmp[i]>=200000:
        if clmp[i]==clumpid:
            x.append(data[i,0])
            y.append(data[i,1])
            z.append(data[i,2])
            vx.append(data[i,3])
            vy.append(data[i,4])
            vz.append(data[i,5])
            ind.append(i)
            counter+=1
    print "found ", counter, "particles in ", beforefile


    unb=np.zeros(len(ind))
    data=np.loadtxt(afterfile, dtype='float', skiprows=1, usecols=[7])
    for i in range(len(ind)):
        if data[ind[i]]>0:
            unb[i]=1
        

    return x,y,z,vx,vy,vz,unb



def get_clump_data(clumpid):

    print "Reading in clump data."

    inputfile=str(argv[4+nphi+2*noutput])        

        # get clump center
    data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,3,4,5,6])
               
    # for i in range(data.shape[0]):
    #     if data[i,0]==clumpid:
    xc=data[1]
    yc=data[2]
    zc=data[3]
    vxc=data[4]
    vyc=data[5]
    vzc=data[6]
            # break

    return xc, yc, zc, vxc, vyc, vzc

def get_cmp(filename):
    print ''
    print " Extracting data from", filename

    data=np.loadtxt(filename, dtype='float', skiprows=1)

    return data[:,0], data[:,1]

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":


    print "Creating figure"
    fig = plt.figure(facecolor='white', figsize=(10,10))
    ax1 = fig.add_subplot(111)
    # ax1.set_yscale('log')
    # ax1.set_xscale('log')

    xc, yc, zc, vxc, vyc, vzc = get_clump_data(clumpid)
   
    ptcls=0
    last_db=0
    last_du=0
    for i in range(noutput):
        x,y,z,vx,vy,vz,unb=get_particles(i,clumpid)
    
        print "Plotting particles"
        dist_b=[]
        dist_u=[]
        vsq_u=[]
        vsq_b=[]
        for j in range(len(x)):
            distance=np.sqrt((x[j]-xc)**2+(y[j]-yc)**2+(z[j]-zc)**2)/500
            vsq=(vx[j]-vxc)**2+(vy[j]-vyc)**2+(vz[j]-vzc)**2

            if unb[j]>0:
                dist_u.append(distance)
                vsq_u.append(0.5*vsq)
            else:
                dist_b.append(distance)
                vsq_b.append(0.5*vsq)


        if(len(dist_u)>0):
            last_du=dist_u[0]
            last_vu=vsq_u[0]

        if(len(dist_b)>0):
            last_db=dist_b[0]
            last_vb=vsq_b[0]

        ax1.scatter(dist_b,vsq_b,c='r',s=1,marker=',',lw=0)
        ax1.scatter(dist_u,vsq_u,c='b',s=1,marker=',',lw=0)
        ptcls+= len(x)

    if (last_db >  0):
        ax1.scatter(last_db,last_vb,c='r',s=1,marker=',',label='bound',lw=0)

    if (last_du > 0):
        ax1.scatter(last_du,last_vu,c='b',s=1,marker=',',label='unbound',lw=0)

    print "Plotted ", ptcls, " particles."

    print "Plotting potential"
    for i in range(nphi):
        inputfile=str(argv[i+4])
        dist,phi=get_phi(inputfile)
        bins=inputfile[-9:]
        bins=bins[:5]
        bins=bins.lstrip("0")
        ax1.loglog(dist/500,(-1)*phi,label="(-1)*potential for "+bins+' mass bins.',c='k')
        # ax1.plot(dist/500,(-1)*phi,label="(-1)*potential for "+bins+' mass bins.',c='k')
 
    
    
    # print "Plotting CMP"
    # 
    # for i in range(nphi):
    #     inputfile=str(argv[i+5+nphi+2*noutput])
    #     print inputfile
    #     dist,mp=get_cmp(inputfile)
    #     bins=inputfile[-9:]
    #     bins=bins[:5]
    #     bins=bins.lstrip("0")
    #     ax1.loglog(dist/500,mp,label="cum. mass profile for "+bins+' mass bins.',c='g')



    ax1.set_xlabel('distances/boxlen')
    ax1.set_ylabel('0.5v^2', size=20)
    ax1.set_title(title, family='serif', size=20) 
    ax1.legend(loc=0, scatterpoints=1,prop=fontP)



    

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"
