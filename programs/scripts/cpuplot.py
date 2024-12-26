#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


# This script plots all particles that are in clumps. It makes 3 subplots,
# one for each plane of coordinates: xy, yz and xz. The particle color is 
# different for every processor.
# It needs mladen_particleoutput.txt* files as they are in this moment 
# (29.06.16), where the first 3 columns are the particle positions and
# the 9th column is the processor ID.
# ( I might rewrite it later so that the procID is read out by which file
# is being read.)
# 
# Usage: cpuplot.py <nproc> <mladen_particleoutput.txt00*>
# <nproc> : number of processors used in ramses run, also the number of 
# output files
# <mladen_particleoutput.txt00*>: all mladen_particleoutput.txt* files.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size


outputfilename = "cpuplot"
workdir= str(getcwd())


noutput=int(argv[1])

print "cpuplot called"





print "Creating figure"

fig = plt.figure(facecolor='white', figsize=(16,6))
ax1 = fig.add_subplot(131, aspect='equal', clip_on=True)
ax2 = fig.add_subplot(132, aspect='equal')
ax3 = fig.add_subplot(133, aspect='equal')

#setting colorbar

fullcolorlist=['black','red', 'green', 'blue', 'gold', 'magenta', 'cyan','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue','silver']

levelmin=0
# #levelmax=int(max(data[:,2]))
levelmax=noutput

bounds=np.linspace(levelmin, levelmax+1,levelmax+2)
colorlist=fullcolorlist[0:levelmax-levelmin+1]
mycmap=matplotlib.colors.ListedColormap(colorlist, name='My colormap')
mynorm=matplotlib.colors.BoundaryNorm(bounds, levelmax+1)




print "Reading in files"
# Read in data, plot one after another
for k in range(0,noutput):
    inputfile=str(argv[k+2])
    data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6])

    if (data.shape[0]>0):
        counter=0
        xd=np.zeros(data.shape[0])
        yd=np.zeros(data.shape[0])
        zd=np.zeros(data.shape[0])

        for i in range(len(data)):
            if data[i,3]>0 :
                xd[counter]=data[i,0]
                yd[counter]=data[i,1]
                zd[counter]=data[i,2]
                counter+=1
                
        
        x=np.zeros(counter)
        y=np.zeros(counter)
        z=np.zeros(counter)

        x=xd[0:counter-1]
        y=yd[0:counter-1]
        z=zd[0:counter-1]

        c=np.zeros(len(x))


        c[:]=float(k+0.25)

        sc=ax1.scatter(x, y, c=c, s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
        
        sc2=ax2.scatter(y, z, c=c, s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
        
        sc3=ax3.scatter(x, z, c=c, s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
        



#--------------------------------

#cmap=plt.cm.jet





# ax1.set_xlim(0.00,1.00)
# ax1.set_ylim(0.00,1.00)  
ax1.set_xlabel('x')
ax1.set_ylabel('y')
# ax2.set_xlim(0.00,1.00)
# ax2.set_ylim(0.00,1.00)  
ax2.set_xlabel('y')
ax2.set_ylabel('z')


# divider = make_axes_locatable(ax1)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
# cax = divider.append_axes("right", size="2%", pad=0.05)
# fig.colorbar(sc, cax=cax)

# divider2 = make_axes_locatable(ax2)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
# cax2 = divider2.append_axes("right", size="2%", pad=0.05)
# fig.colorbar(sc2, cax=cax2)


# ax3.set_xlim(0.00,1.00)
# ax3.set_ylim(0.00,1.00)      
ax3.set_xlabel('x')
ax3.set_ylabel('z')

# divider3 = make_axes_locatable(ax3)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
# cax3 = divider3.append_axes("right", size="2%", pad=0.05)
# fig.colorbar(sc3, cax=cax3)

#plt.colorbar(sc)

plt.tight_layout()
print "Figure created"


# saving figure
fig_path = workdir+'/'+outputfilename+'.png'
print "saving figure as "+fig_path
plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
plt.close()

print "done", outputfilename+".png"

