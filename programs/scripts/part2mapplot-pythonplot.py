#!/usr/bin/python

# This script is called by the part2mapplot script and will create a graph of the (hop) part2map (mass) output.

from numpy import loadtxt, array, sqrt
from os import getcwd
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
from sys import argv #command line arguments
from matplotlib import pyplot
from matplotlib.colors import LogNorm, Normalize
import subprocess


filename = str(argv[1])
outputfilename = str(argv[2])
xlabel=str(argv[3])
ylabel=str(argv[4])
title=str(argv[5])
workdir= str(getcwd())


if (outputfilename == '12345'):
    outputfilename = filename


def extract_ascii(filename):
    """
    Extract the hop map data from an ascii file
    Thanks Philipp Denzel!

    """
    # First line of file gives map dimensions nx, ny
    #awk_callwindow = ['awk', 'NR==1{print $1; print $2}', getcwd()+'/'+filename]
    #p1 = subprocess.Popen(awk_callwindow, stdout=subprocess.PIPE)
    #stdout_val = p1.communicate()[0]
    #p1.stdout.close()
    #[nx, ny] = list(map(int, stdout_val.split()))
    # extract map data with awk
    awk_callmap = ['awk', ' {print $3} ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    data_map = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln

    #sortierte data_map erstellen um kleinsten Wert != 0 zu erhalten
    sorted_map= sorted(data_map)
    data_map = array(data_map)
    maxvalue = data_map.max()   

    iszero = True
    index = 0
    while (iszero): #if value=0, assign value/=0. 
        if (sorted_map[index] == 0):
            sorted_map[index] = maxvalue
            index += 1
        else:
            minvalue = sorted_map[index]
            iszero = False
       
    sorted_map = array(sorted_map)
    #minvalue = sorted_map.min()
       # sort out any 0s in case there are some
    
    data_map_without_zeros = array([])
    for i in range(0, len(data_map)):
        if data_map[i] == 0.0:
            data_map[i] = minvalue

    gridsize = sqrt(len(data_map))

    
    # reshape data for imshow
    data_map = data_map.reshape(gridsize, gridsize)

    # search min/max for colorbar
    
    return data_map, minvalue, maxvalue, gridsize


# create data_map from part2map .map file
print "importing data"
data_map, minvalue, maxvalue, gridsize = extract_ascii(filename)
print "data imported"



print "creating figure"
print "gridsize", gridsize


# instantiate new figure and axis objects
fig = pyplot.figure(facecolor='white', figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.axis([0, gridsize, 0, gridsize])

# plot it
im = ax.imshow(data_map, interpolation='none', cmap='jet', norm=LogNorm(), origin="lower")
ax.set_xticklabels([0, "", "","","",1])
ax.set_yticklabels([0, "", "","","",1])

# ax.set_title(title, size=40, y=1.04,  family='serif')
xlabel='x'
ylabel='y'
ax.set_xlabel(xlabel, size=20, labelpad=20, family='serif')
ax.set_ylabel(ylabel, size=20, labelpad=20, family='serif')

fig.colorbar(im, fraction=0.046, pad=0.04)
fig.tight_layout()

fig_path = workdir+'/'+outputfilename+'.png'
print "saving figure as"+fig_path
pyplot.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=100)
pyplot.close()

print "done"



