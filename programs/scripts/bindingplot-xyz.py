#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


# This script will plot all particles from a ramses output,
# where their color will represent their level. (the level
# in which the clump they belong to is in.)


from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size


outputfilename = "particle_binding_plot"
workdir= str(getcwd())


noutput=int(argv[1])

print "bindingplot-xyz.py called"
print "Reading in files"

for i in range(0,noutput):
    inputfile=str(argv[i+2])
    temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,8])
    if (i == 0):
       data = temp_data
    else:
       data = np.concatenate((data, temp_data), axis=0)

levelmin=int(min(data[:,2]))
#levelmax=int(max(data[:,2]))
levelmax=20


print "Creating figure"

fig = plt.figure(facecolor='white', figsize=(16,6))
ax1 = fig.add_subplot(131, aspect='equal', clip_on=True)
ax2 = fig.add_subplot(132, aspect='equal')
ax3 = fig.add_subplot(133, aspect='equal')

#setting colorbar

fullcolorlist=['black','red', 'green', 'blue', 'gold', 'magenta', 'cyan','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue','silver']


#--------------------------------

#cmap=plt.cm.jet

bounds=np.linspace(levelmin, levelmax+1,levelmax+2)
colorlist=fullcolorlist[0:levelmax-levelmin+1]
mycmap=matplotlib.colors.ListedColormap(colorlist, name='My colormap')
mynorm=matplotlib.colors.BoundaryNorm(bounds, levelmax+1)




sc=ax1.scatter(data[:,0], data[:,1], c=data[:,3], s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
ax1.set_xlim(0.00,1.00)
ax1.set_ylim(0.00,1.00)  
ax1.set_xlabel('x')
ax1.set_ylabel('y')


divider = make_axes_locatable(ax1)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
cax = divider.append_axes("right", size="2%", pad=0.05)
fig.colorbar(sc, cax=cax)




sc2=ax2.scatter(data[:,1], data[:,2], c=data[:,3], s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
ax2.set_xlim(0.00,1.00)
ax2.set_ylim(0.00,1.00)  
ax2.set_xlabel('y')
ax2.set_ylabel('z')



divider2 = make_axes_locatable(ax2)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
cax2 = divider2.append_axes("right", size="2%", pad=0.05)
fig.colorbar(sc2, cax=cax2)







sc3=ax3.scatter(data[:,0], data[:,2], c=data[:,3], s=0.1, alpha=1, marker=",", lw=0, norm=mynorm, vmin=levelmin, vmax=levelmax+1, cmap=mycmap)
ax3.set_xlim(0.00,1.00)
ax3.set_ylim(0.00,1.00)      
ax3.set_xlabel('x')
ax3.set_ylabel('z')

divider3 = make_axes_locatable(ax3)
#colorbarsize=bigger/(12.0*150)
#cax = divider.append_axes("right", size=colorbarsize, pad=0.05)
cax3 = divider3.append_axes("right", size="2%", pad=0.05)
fig.colorbar(sc3, cax=cax3)

#plt.colorbar(sc)

plt.tight_layout()
print "Figure created"


# saving figure
fig_path = workdir+'/'+outputfilename+'.png'
print "saving figure as "+fig_path
plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
plt.close()

print "done", outputfilename+".png"

