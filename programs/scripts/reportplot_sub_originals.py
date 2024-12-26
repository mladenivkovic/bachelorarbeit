#!/usr/bin/python

# Creates a 3D scatterplot of the originally set up clumps.
# usage: reportplot_sub_originals.py haloparticle-file subhaloparticle-file subsubhaloparticle-files

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
from matplotlib.pyplot import subplots_adjust

outputfilename = "dice_sub_original-plot"
workdir= str(getcwd())


halofile=str(argv[1])

fullcolorlist=m.fullcolorlist


halodata=np.loadtxt(halofile, dtype='float', skiprows=1, usecols=[0,1,2])
halox=halodata[:,0]
haloy=halodata[:,1]
haloz=halodata[:,2]



fig = plt.figure(facecolor='white', figsize=(10,10.5))
ax1 = fig.add_subplot(111, projection='3d')


pointsize=.4
mylw=0.0
mymarker=','
pointalpha=0.2

counter=0
halolabel=r'halo-namegiver particles'
ax1.scatter(halox,haloy,haloz,s=pointsize,c=fullcolorlist[counter], label=halolabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)


for i in range(len(argv)-2):
    clumpfile=str(argv[2+i])
    clumpdata=np.loadtxt(clumpfile, dtype='float', skiprows=1, usecols=[0,1,2])
    counter=1+i
    if (i==0):  
        clumplabel='subhalo particles'
        pointsize=0.5
        pointalpha=.3
    else:
        clumplabel='subsubhalo '+str(i)+' particles'
        pointsize=1
        pointalpha=.6

    ax1.scatter(clumpdata[:,0], clumpdata[:,1], clumpdata[:,2],s=pointsize,c=fullcolorlist[counter], label=clumplabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)





ax1.view_init(azim=5, elev=15.)
# ax1.view_init(elev=60,azim=340)

#label axes
ax1.set_xlim3d(0,800)
ax1.set_ylim3d(0,800)
ax1.set_zlim3d(0,800)

#label axes
ax1.set_xlabel(r'x $[kpc]$', labelpad=2, family='serif',size=24)
ax1.set_ylabel(r'y $[kpc]$', labelpad=2, family='serif',size=24)
ax1.zaxis.set_rotate_label(False)
ax1.set_zlabel(r'z $[kpc]$', labelpad=5, family='serif',size=24,rotation=90)

ax1.set_xticklabels([0,"","","","","","","",800],va='bottom',ha='left')
ax1.set_yticklabels([0,"","","","","","","",800],va='baseline',ha='right')
ax1.set_zticklabels([0,"","","","","","","",800],va='baseline',ha='right')

# set tick params (especially digit size)
ax1.tick_params(axis='both',which='major',labelsize=18,pad=3)


subplots_adjust(left=-0.17, right=1.17, top=1.00, bottom=-0.10,wspace=0.00,hspace=0.00)

legloc = 'upper right'
bbox_to_anchor=(0.55, 0.99)
legsize = 22







ax1.grid(True)
ax1.w_xaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
ax1.w_yaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
ax1.w_zaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
ax1.w_xaxis.set_pane_color(( 0,0.1,0.7,.15))
ax1.w_yaxis.set_pane_color(( 0,0.1,0.7,.15))
ax1.w_zaxis.set_pane_color(( 0,0.1,0.7,.15))

fontP=FontProperties()
fontP.set_size(legsize)
fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

lgnd1=ax1.legend(scatterpoints=1,prop=fontP, fancybox=True, framealpha=1, bbox_to_anchor=bbox_to_anchor)

for l in range(len(lgnd1.legendHandles)):
    lgnd1.legendHandles[l]._sizes = [30]
    lgnd1.legendHandles[l].set_alpha(1)



this_name=outputfilename
m.save_fig(this_name,fig,workdir)

