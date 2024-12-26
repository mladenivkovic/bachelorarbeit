#!/usr/bin/python

# This script is called by the  part2map (mass) output file of cosmo runs.

from numpy import loadtxt, array, sqrt
from os import getcwd
from sys import argv #command line arguments
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.axes_grid1 import make_axes_locatable



filename = str(argv[1])
which = int(argv[2])

title=r"Projection of number of particles along $z$ axis"
workdir= str(getcwd())

cmap='gnuplot2'







# set up for which case to work

if which == 1: #cosmo
    ticks = [1,10,100,500]
    ticklabels = ['1','10','100','500']
    axx = [0, 1]
    axy = [0, 1]
    xlabel="x"
    ylabel="y"
    pmass = 4.7683715820312500E-007
    outputfilename = "cos-part2map-npart"

elif which == 2:  #dice two

    axx = [0, 500]
    axy = [0, 500]

    xlabel="kpc"
    ylabel="kpc"
    pmass = 5.0000002374872574E-003
    outputfilename = "dice-two-part2map-npart"

elif which == 3:    # dice sub
    axx = [0, 1000]
    axy = [0,1000]

    xlabel="kpc"
    ylabel="kpc"
    pmass = 5.0000002374872574E-003
    outputfilename = "dice-sub-part2map-npart"



def extract_ascii(filename):

    val = loadtxt(filename,dtype='float',unpack=True,usecols=([2]))
    print len(val)


    minvalue=0.4
    sumcheck=0

    for i,m in enumerate(val):
        if m==0:
            val[i]=minvalue
        else:
            val[i]=m/pmass
            sumcheck += val[i]


    print "sumcheck", sumcheck #should be close to number of particles in simulation
    maxvalue=max(val)

    gridsize=int(sqrt(len(val)))
    data_map = val.reshape((gridsize,gridsize))


    return data_map, minvalue, maxvalue, gridsize


# create data_map from part2map .map file
print "importing data"
data_map, minvalue, maxvalue, gridsize = extract_ascii(filename)
print "data imported"



print "creating figure"
print "gridsize", gridsize, "max:", maxvalue


# instantiate new figure and axis objects
fig = plt.figure(facecolor='white', figsize=(11,10))
ax = fig.add_subplot(1,1,1)
# ax.axis([0.005, gridsize, 0.005, gridsize])
ax.axis([1, gridsize, 1, gridsize])



# plot it
im = ax.imshow(data_map, interpolation='lanczos', cmap=cmap,vmin=minvalue,vmax=maxvalue, norm=LogNorm(), origin="lower",aspect='equal')

# say where you want the axis ticks (make only 2):
plt.xticks([0,gridsize])
plt.yticks([0,gridsize])

# label the axis ticks:
ax.set_xticklabels(axx)
ax.set_yticklabels(axy)

ax.set_title(title, size=16,  family='serif')#y=1.04, 
ax.set_xlabel(xlabel, size=16, labelpad=5, family='serif')
ax.set_ylabel(ylabel, size=16, labelpad=5, family='serif')

# COLORBAR
divider = make_axes_locatable(ax)
cax= divider.append_axes("right",size="2.5%",pad=0.10)

cbar = fig.colorbar(im, cax=cax)
if which == 1:
    cbar = fig.colorbar(im, ticks=ticks,cax=cax)
    cbar.ax.set_yticklabels(ticklabels)  # vertically oriented colorbar



fig.tight_layout()



# SAVE FIGURE
fig_path = workdir+'/'+outputfilename+'.png'
print "saving figure as"+fig_path
plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=100,bbox_inches='tight')
plt.close()

print "done"



