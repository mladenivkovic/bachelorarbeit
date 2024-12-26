#!/usr/bin/python

from os import getcwd
from sys import argv #command line arguments
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
import warnings
from matplotlib.font_manager import FontProperties # for legend
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
from mpl_toolkits.mplot3d import Axes3D
import report_module as m

outputfilename = "dice_two_original-plot"
workdir= str(getcwd())


halofile=str(argv[1])
clumpfile=str(argv[2])

fullcolorlist=m.fullcolorlist

halodata=np.loadtxt(halofile, dtype='float', skiprows=1, usecols=[0,1,2])
halox=halodata[:,0]
haloy=halodata[:,1]
haloz=halodata[:,2]

clumpdata=np.loadtxt(clumpfile, dtype='float', skiprows=1, usecols=[0,1,2])


fig = plt.figure(facecolor='white', figsize=(10,10.5))
ax1 = fig.add_subplot(111, projection='3d')


pointsize=1.5
mylw=0.0
mymarker=','
pointalpha=0.2

counter=0
halolabel=r'halo-namegiver particles'
ax1.scatter(halox,haloy,haloz,s=pointsize,c=fullcolorlist[counter], label=halolabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)

pointsize=2
pointalpha=.6
counter=1
clumplabel=r'subhalo particles'
ax1.scatter(clumpdata[:,0], clumpdata[:,1], clumpdata[:,2],s=pointsize,c=fullcolorlist[counter], label=clumplabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)


m.tweak_plot_3D(fig,plt, ax1,'two')


this_name=outputfilename
m.save_fig(this_name,fig,workdir)

plt.close()

