#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


# plot cumulative mass profiles.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
import unbinding_module as m
import warnings

outputfilename = "CMP-plot"
workdir= str(getcwd())
# pm=3.814697265625000E-006 ## WILL BE DIFFERENT!

noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])




def get_cmp(halo, children,noutput):
    #-------------
    # get data
    #-------------

    print "Reading in CMP files"


    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
        
        # get clump center
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[1,2,3,4,5,6,7,8,9,10])

        if(temp_data.shape[0]>0):
            if 'data' in locals():
                data = np.vstack((data, temp_data))
            else:
                data = temp_data
        

        #get clump ids, parents and levels
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0])
        if(temp_data_int.shape[0]>0):
            if 'data_int' in locals():
                data_int= np.concatenate((data_int, temp_data_int))
            else:
                data_int = temp_data_int


    # if not (type(data_int) in [tuple, list]):
    #     data_int = [data_int]


    cmps=[]
    ids=[]

    print data
    print data_int
    print children

    for k in range(len(data_int)):
        for l in range(len(children)):
            if (data_int[k] == children[l]):
                cmps.append(data[k,:])
                ids.append(data_int[k])

    return ids,cmps














#--------------------------------

def createfig(ids,cmps):
    print "Creating figure"


    x = range(1,11)

    fontP=FontProperties()
    fontP.set_size('xx-small') 
    fontP.set_family('monospace') 

    fig = plt.figure(facecolor='white', figsize=(6,6))
    fig.suptitle('Cumulative Mass Profiles', fontsize='20', family='serif')


    ax1=plt.subplot(111)

    for k in range(len(ids)):
        ax1.semilogy(x, cmps[k],c=m.fullcolorlist[k], label=str(ids[k]))
    ax1.set_xlabel('Distance bin to CoM')
    ax1.set_ylabel('Cumulative mass')

    ax1.grid(True)
    ax1.legend(loc=2,prop=fontP, title='clump id', framealpha=0.5) 



    # plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05,wspace=0.3,hspace=0.3)

    # plt.tight_layout()
    print "Figure created"
    return fig











if __name__ == "__main__":

    children,child_levels,clumpx,clumpy,clumpz = m.get_clump_data(halo, noutput)
    ids, cmps = get_cmp(halo, children,noutput)
    fig=createfig(ids,cmps)

    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=200)
    plt.close()

    print "done", outputfilename+".png"

