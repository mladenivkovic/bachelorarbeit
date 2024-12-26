#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


# plot cumulative mass profiles for linear binning. 

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend


outputfilename = "CMP-lin-plots"
workdir= str(getcwd())


print "cmp-lin.py called"


#-------------
# get data
#-------------

print "Reading in files"

inputfile=str(argv[1])
print inputfile
data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[1,2,3,4,5,6,7,8,9,10])
clumpid=np.loadtxt(inputfile,dtype='int',skiprows=1,usecols=[0])

pm=3.814697265625000E-006 ## WILL BE DIFFERENT!

clumpid=[clumpid]

#setting colorbar

fullcolorlist=['black','red', 'green', 'blue', 'gold', 'magenta', 'cyan','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue']

clrs=len(fullcolorlist)
# peaks=len(clumpid)
peaks=1
totalplots=1
calc=clrs
while(calc<peaks):
    totalplots+=1
    calc=totalplots*clrs

r=[]
c=[]
for i in range(1,totalplots+1):
    if (totalplots%i==0):
        r.append(totalplots/i)
        c.append(i)

difference=[]

for i in range(0, len(r)):
    difference.append(abs(r[i]-c[i]))

rows=r[difference.index(min(difference))]
columns=c[difference.index(min(difference))]

if (rows>columns):
    save=rows
    rows=columns
    columns=save



#--------------------------------
print "Creating figure"



x = range(1,11)

fontP=FontProperties()
fontP.set_size('xx-small') 
fontP.set_family('monospace') 

fig = plt.figure(facecolor='white', figsize=(5*columns,5*rows*2+0.5))
fig.suptitle('Cumulative Mass Profiles for linear bins', fontsize='20', family='serif')

for p in range(1,totalplots):

    ax1=plt.subplot(2*rows,columns,p)
    ax2=plt.subplot(2*rows,columns,p+totalplots)

    for cl in range(0,clrs):
        index=(p-1)*clrs+cl
        if (index<peaks):
            ax1.semilogy(x, data[index],c=fullcolorlist[cl], label=str(clumpid[index]))
            ax2.semilogy(x, data[index]/pm,c=fullcolorlist[cl],label=str(clumpid[index])) 
        ax1.set_xlabel('Distance bin to CoM')
        ax1.set_ylabel('Cumulative mass')
        ax2.set_xlabel('Distance bin to CoM')
        ax2.set_ylabel('Cumulative mass in units of particle mass')

        ax1.grid(True)
        ax1.legend(loc=8,prop=fontP, title='clump id',ncol=clrs/5+1, framealpha=0.5) 
        ax2.grid(True)
        ax2.legend(loc=8,prop=fontP, title='clump id',ncol=clrs/5+1, framealpha=0.5) 



plt.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.05,wspace=0.3,hspace=0.3)

# plt.tight_layout()
print "Figure created"


# saving figure
fig_path = workdir+'/'+outputfilename+'.png'
print "saving figure as "+fig_path
plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=200)
plt.close()

print "done", outputfilename+".png"

