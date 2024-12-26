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

noutput=int(argv[1])
# clumpid=int(argv[2])
workdir= str(getcwd())
pot=workdir[-15:]
binning=pot[-7:]
pot=pot[:7]
outputfilename = "filtered_particles.txt"




def get_particles(counter):
    # READ CLUMP DATA IN FIRST
    beforefile=str(argv[counter+2])
    # afterfile=str(argv[counter+2+nphi+noutput])
    print "Reading in particle data"
    x=[]
    y=[]
    z=[]
    vx=[]
    vy=[]
    vz=[]
    idp=[]
    clumpidp=[]
    ind=[]



    data=np.loadtxt(beforefile, dtype='float', skiprows=1, usecols=[0,1,2,3,4,5,6])
    clmp=np.loadtxt(beforefile,dtype='int',skiprows=1,usecols=[6])
    idp=np.loadtxt(beforefile,dtype='int',skiprows=1,usecols=[9])
    
    counter=0
    for i in range(data.shape[0]):
        # if idp[i]>240000 and idp[i]<=260000:  #filter condition
        # if idp[i]>200000:  #filter condition
        if idp[i]<=200000:  #filter condition
        # if clmp[i]==clumpid:
            x.append(data[i,0])
            y.append(data[i,1])
            z.append(data[i,2])
            vx.append(data[i,3])
            vy.append(data[i,4])
            vz.append(data[i,5])
            clumpidp.append(clmp[i])
            ind.append(idp[i])
            counter+=1
    print "found ", counter, "particles in ", beforefile


    # unb=np.zeros(len(ind))
    # data=np.loadtxt(afterfile, dtype='float', skiprows=1, usecols=[7])
    # for i in range(len(ind)):
    #     if data[ind[i]]>0:
    #         unb[i]=1
        

    return x,y,z,vx,vy,vz,clumpidp,ind



if __name__ == "__main__":
    

    f=open(outputfilename,'w')

    counter=0
    for i in range(noutput):
        x,y,z,vx,vy,vz,clmpid,ind=get_particles(i)
        counter+=len(x)
        for i in range(len(x)):
            f.write('{0:18.10f}{1:18.10f}{2:18.10f}{3:18.10f}{4:18.10f}{5:18.10f}{6:10d}{7:10d}'.format(x[i],y[i],z[i],vx[i],vy[i],vz[i],clmpid[i],ind[i]))
            f.write('\n')
            
    print counter
