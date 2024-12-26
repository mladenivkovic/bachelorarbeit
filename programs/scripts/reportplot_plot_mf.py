#!/usr/bin/python
from os import getcwd
from sys import argv #command line arguments
import numpy as np
import matplotlib.pyplot as plt
import report_module as r

workdir= str(getcwd())


outputfilename = "subclump_mass_function"


if __name__ == "__main__":
    clst=r.fullcolorlist
    fig = plt.figure(facecolor='white', figsize=(20,20))
    ax1 = fig.add_subplot(111, aspect='equal')
    names=['Unbinding neglecting neighbours', 'PHEW segmentation','Unbinding with neighbour correction']
    maxbins=0
    for j in range(1,len(argv)):
        data=np.loadtxt(argv[j],dtype='int',usecols=[0,1])
        bins=data[:,0]
        values=data[:,1]
        name=names[j-1]+': '+str(int(sum(values)/2))+' clumps'
        ax1.loglog(bins,values,c=clst[j-1],label=name,alpha=1)
        print argv[j], names[j-1]
        maxbins=max(maxbins,bins[-1])


    ax1.set_xlim(0.5,5*maxbins)
    ax1.set_ylim(0.5,1e3)
    r.tweak_plot_2D(fig,plt,ax1,'mf')
    r.save_fig(outputfilename, fig,workdir)
        

