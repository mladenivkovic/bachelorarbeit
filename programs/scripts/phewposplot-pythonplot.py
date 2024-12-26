#!/usr/bin/python

# This script is called by the phewposplot script and will create a graph of the phew halo_XXXXX.-allinone.dat file (which is created by the phewposplot script)  with approximated halo sizes.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt


filename = str(argv[1])
outputfilename = str(argv[2])
xlabel=str(argv[3])
ylabel=str(argv[4])
title=str(argv[5])
workdir= str(getcwd())


def extract_ascii(filename):
    # Per default, I extract x and y coordinates.
    # To change that, change the column numbers that awk reads in:
    # x = $3, y = $4, z = $5


    print "extracting data"
    # Extract x coordinates
    awk_callmap = ['awk', ' NR > 1 { print $3 } ', getcwd()+'/'+filename]
    p1 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p1.communicate()[0]
    p1.stdout.close()
    xcoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    xcoord = np.array(xcoord)

    # Extract y coordinates
    awk_callmap = ['awk', ' NR > 1 { print $4 } ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    ycoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    ycoord = np.array(ycoord)

    # Extract mass
    awk_callmap = ['awk', ' NR > 1 {print $7} ', getcwd()+'/'+filename]
    p3 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p3.communicate()[0]
    p3.stdout.close()
    mass = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    mass = np.array(mass) 
    
    print "data imported"
    return xcoord, ycoord, mass


def radius(mass):
    
    #Calculating the area of the halo for the scatterplot, assuming halo has density 200. Comes from M_halo = 4/3 pi * r^3 * 200
    radius = np.zeros(len(mass))
    print "calculating halo area"
    for i in range(0, len(mass)-1):
        calc = (3 * mass[i] / 800.0 * np.pi) **(1./3)
        radius[i] = calc
    return radius



if __name__ == "__main__":

    print "Creating figure"

    fig = plt.figure(facecolor='white', figsize=(15,15))
    ax = fig.add_subplot(1,1,1)
    ax.axis([0, 1, 0, 1])
#    ax.set_xlim(0.00,1.00)
#    ax.set_ylim(0.00,1.00)
#    ax.set_clip_on(True)

    ax.axis('scaled') 
    #setting up an empty scatterplot for pixel reference
    xedges=[0.000, 1.000]
    yedges=[0.000, 1.000]
    emptyscatter=ax.scatter(xedges, yedges, s=0.0)
    ax.set_xlim(0.00,1.00)
    ax.set_ylim(0.00,1.00)    
    # Calculating the ratio of pixel-to-unit
    xy_pixels = ax.transData.transform(np.vstack([xedges,yedges]).T)
    xpix, ypix = xy_pixels.T
    x_to_pix_ratio = (xpix[1] - xpix[0])
    y_to_pix_ratio = (ypix[1] - ypix[0])

    # Take the mean value of the ratios because why not 
    dist_to_pix_ratio = (x_to_pix_ratio + y_to_pix_ratio) / 2.0

    # Extract data
    x, y, mass = extract_ascii(filename)

    # Calculate radius
    radius = radius(mass)
   
    # Calculate marker size
    halosize = np.zeros(len(radius))
    for i in range(0, len(radius)):
        calc = (radius[i]*dist_to_pix_ratio)**2
        halosize[i] = calc
        

    # Plot it
    ax.scatter(x, y, s=halosize, alpha=0.4, lw=0)
    ax.set_xlim(0.00,1.00)
    ax.set_ylim(0.00,1.00)   

    #Set title and axis labels
    ax.set_title(title, size=40, y=1.04,  family='serif')
    ax.set_xlabel(xlabel, size=20, labelpad=20, family='serif')
    ax.set_ylabel(ylabel, size=20, labelpad=20, family='serif')

    print "Figure created"

    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"
