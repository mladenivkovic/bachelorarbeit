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

infile=str(argv[1])
outputfilename = "subclump-profile"
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

    data=np.loadtxt(infile, dtype='float', skiprows=0, usecols=[0,1,2,3,4,5])


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



def nfw(r,maxdist,totalmass):

    a=maxdist/c
    rho_0=totalmass/(4*np.pi*a**3*(np.log(1+maxdist/a)-1/(a/maxdist+1)))
    M=4*np.pi*rho_0*a**3*( np.log(1+r/a)-1/(a/r+1))
    return M

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    x,y,z,vx,vy,vz=get_particles(infile)
    xc, yc, zc, vxc, vyc, vzc = get_clump_data(x,y,z,vx,vy,vz)
    xc=xc0
    yc=yc0
    zc=zc0
    bins,massprof,dist=get_cmp(x,y,z,xc,yc,zc)
    maxdist=dist[-1]
    totalmass=massprof[-1]
    print maxdist,totalmass,totalmass/m, len(x)


    # dist=dist/boxlen



#     print "Creating figure"
    fig = plt.figure(facecolor='white', figsize=(10,10))
    ax1 = fig.add_subplot(111)
    # ax1.plot(bins,massprof)
    # ax1.set_yscale('log')
    # ax1.set_xscale('log')
    vsq=np.zeros(len(x))
    for i in range(len(x)):
        vsq[i]=(vx[i]-vxc)**2+(vy[i]-vyc)**2+(vz[i]-vzc)**2 
        # vsq[i]=np.sqrt( (vx[i]-vxc)**2+(vy[i]-vyc)**2+(vz[i]-vzc)**2 )

  
    r_nfw=np.zeros(len(bins)) 
    for i in range(len(bins)):
        r_nfw[i]=i*r200/len(bins)


    ax1.scatter(dist/boxlen,vsq,c='r',s=1,marker=',',lw=0,label='v^2 of particles')
    # ax1.loglog(bins/boxlen,gmr,c='b',label='GM(<r)/r')
    # ax1.loglog(bins/boxlen,gm2r,c='k',label='2*GM(<r)/r')
    # ax1.loglog(bins/boxlen,-phi,c='g',label='poisson potential')
    ax1.loglog(bins/boxlen,massprof,c='b',label='cum mass profile from binning')
    ax1.loglog(r_nfw/boxlen,nfw(r_nfw,r200,totalmass),c='k',label="expected NFW profile")
 

    ax1.set_xlabel('distances/boxlen')
    ax1.set_ylabel('(-1)*potential // E_kin', size=20)
    ax1.set_title(title, family='serif', size=20) 
    ax1.legend(loc=0, scatterpoints=1,prop=fontP)
 
 
 
    # print gm2r[-1], gmr[-1] 
    # print "Bulk velocity", np.sqrt(vxc**2+vyc**2+vzc**2) 
    print "CoM"
    print xc, yc, zc
    print xc*length, yc*length, zc*length
    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()
# 
    print "done", outputfilename+".png"
