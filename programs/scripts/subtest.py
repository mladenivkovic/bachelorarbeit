#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This scripts plots the particles by distance and their
# kinetic energy as well as their calculated potential.
# inputfile is filtered particle file created by
# filterparticles.py
# Usage: subtest.py inputfile.txt



from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import warnings as warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend

infile=str(argv[1])
outputfilename = "subclump_potentials"
title="reconstructed clump properties"
workdir= str(getcwd())


#dice data
m=5.000000237487257E-003
boxlen=500

c=9.79
xc0=70.7+250
yc0=250.0
zc0=250.0-70.7
r200=119.5

nbins=10000
length=0.308567758128200E+22
parsec=3.086e+18 #pc in cm

#Legend stuff
fontP=FontProperties()
fontP.set_size('x-small') # sizes = ['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']



def get_particles(infile):
    print "Reading in particle data"

    data=np.loadtxt(infile, dtype='float', skiprows=1, usecols=[0,1,2,3,4,5])

    x=data[:,0]
    y=data[:,1]
    z=data[:,2]
    vx=data[:,3]
    vy=data[:,4]
    vz=data[:,5]

    return x,y,z,vx,vy,vz






def get_clump_data(x,y,z,vx,vy,vz):

    xc=sum(x)/len(x)
    yc=sum(y)/len(y)
    zc=sum(z)/len(z)
    vxc=sum(vx)/len(x)
    vyc=sum(vy)/len(y)
    vzc=sum(vz)/len(z)


    return xc, yc, zc, vxc, vyc, vzc




def get_cmp(x,y,z,xc,yc,zc):
    bins=np.zeros(nbins+1)
    massprof=np.zeros(nbins+1)
    maxdist=np.sqrt((x[0]-xc)**2+(y[0]-yc)**2+(z[0]-zc)**2)
    dist=np.zeros(len(x)) 
    for i in range(len(x)):
        dist[i]=(x[i]-xc)**2+(y[i]-yc)**2+(z[i]-zc)**2
        dist[i]=np.sqrt(dist[i])
        if maxdist<dist[i]:
            maxdist=dist[i]

    bins[nbins]=maxdist
    bins[0]=0
    delta=maxdist/float(nbins)
    for i in range(nbins):
        bins[i]=i*delta

    for i in range(len(x)):
        for j in range(nbins+1):
            ibin=j
            if bins[j]>dist[i]:
                break

        massprof[ibin]+=m
   
    for i in range(nbins):
        massprof[i+1]+=massprof[i]


    return bins, massprof, dist

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    x,y,z,vx,vy,vz=get_particles(infile)
    xc, yc, zc, vxc, vyc, vzc = get_clump_data(x,y,z,vx,vy,vz)
    #overwrite 
    xc=xc0
    yc=yc0
    zc=zc0
    bins,massprof,dist=get_cmp(x,y,z,xc,yc,zc)
    # dist=dist/boxlen



#     print "Creating figure"
    fig = plt.figure(facecolor='white', figsize=(10,10))
    ax1 = fig.add_subplot(111)
    # ax1.plot(bins,massprof)
    # ax1.set_yscale('log')
    # ax1.set_xscale('log')
    vsq=np.zeros(len(x))
    for i in range(len(x)):
        vsq[i]=np.sqrt( (vx[i]-vxc)**2+(vy[i]-vyc)**2+(vz[i]-vzc)**2 )

    gmr=np.zeros(nbins+1)
    phi=np.zeros(nbins+1)

    for j in range(nbins):
        gmr[j+1]=np.sqrt(massprof[j+1]/bins[j+1])
        delta=bins[j+1]-bins[j]
        phi[j+1]=-massprof[j+1]/bins[j+1]**2*delta

    addterm=-massprof[-1]/bins[-1]
    ind=nbins-1
   
    #calculate poisson potential
    print phi[-1], "--1"
    for j in range(nbins):
        i=ind-j
        phi[i]+=phi[i+1]
        phi[i+1]+=addterm
    print phi[-1], "--1"

    phi[0]=phi[1]+addterm

    for j in range(len(phi)):
        phi[j]=np.sqrt(-2*phi[j])

    gm2r=np.zeros(nbins+1)
    # gm3r=np.zeros(nbins+1)
    for j in range(nbins+1):
        gm2r[j]=np.sqrt(2)*gmr[j]
        # gm3r[j]=3*gmr[j]
   
    # print phi


    ax1.scatter(dist/boxlen,vsq,c='r',s=1,marker=',',lw=0,label='|v| of particles')
    ax1.loglog(bins/boxlen,gmr,c='b',label='sqrt[GM(<r)/r]')
    ax1.loglog(bins/boxlen,gm2r,c='k',label='sqrt[2*GM(<r)/r]')
    # ax1.loglog(bins/boxlen,gm3r,c='g',label='3*sqrt[GM(<r)/r]')
    ax1.loglog(bins/boxlen,phi,c='g',label='sqrt[-2phi]')
 
    ax1.set_xlabel('distances/boxlen')
    ax1.set_ylabel('v', size=20)
    ax1.set_title(title, family='serif', size=20) 
    ax1.legend(loc=0, scatterpoints=1,prop=fontP)
 
 
 
    # print gm2r[-1], gmr[-1] 
    print "Bulk velocity", np.sqrt(vxc**2+vyc**2+vzc**2) 
    print "CoM"
    print xc, yc, zc
    # print xc*length, yc*length, zc*length
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()
# 
    print "done", outputfilename+".png"
