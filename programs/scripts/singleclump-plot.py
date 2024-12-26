#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script will plot the clump(s) found by phew and estimated clump size along with all the particles found by me so I can compare, but only for a chosen clump.

# Usage: execute the corresponding bash script.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt


workdir= str(getcwd())
clumpid=str(argv[1])
clumpfile=argv[2]
particlefile=argv[3]
outputfilename = "particle_clump_comparison_id"+clumpid
title='Particle clump comparison clump '+clumpid

def extract_ascii_clumpfinder(filename):
    # Per default, I extract x and y coordinates.
    # To change that, change the column numbers that awk reads in:
    # x = $5, y = $6, z = $7

    print "extracting clumpfinder data from file", filename
    # Extract x coordinates
    awk_callmap = ['awk', ' NR > 1 { print $6 } ', getcwd()+'/'+filename]
    p1 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p1.communicate()[0]
    p1.stdout.close()
    xcoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    xcoord = np.array(xcoord)

    # Extract y coordinates
    awk_callmap = ['awk', ' NR > 1 { print $7 } ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    ycoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    ycoord = np.array(ycoord)

    # Extract mass
    awk_callmap = ['awk', ' NR > 1 {print $12} ', getcwd()+'/'+filename]
    p3 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p3.communicate()[0]
    p3.stdout.close()
    mass = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    mass = np.array(mass) 
    
    print "clumpfind data imported"
    return xcoord, ycoord, mass




def extract_ascii_particles(filename):

    print "extracting particle data from file", filename
    # Extract x coordinates
    awk_callmap = ['awk', ' NR > 1 { print $1 } ', getcwd()+'/'+filename]
    p1 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p1.communicate()[0]
    p1.stdout.close()
    xcoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    xcoord = np.array(xcoord)

    # Extract y coordinates
    awk_callmap = ['awk', ' NR > 1 { print $2 } ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    ycoord = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    ycoord = np.array(ycoord)

    print "particle data imported"
    return xcoord, ycoord

def radius(mass):
    
    #Calculating the area of the halo for the scatterplot, assuming halo has density 200. Comes from M_halo = 4/3 pi * r^3 * 200
    radius = np.zeros(len(mass))
    print "calculating clump area"
    for i in range(0, len(mass)):
        calc = (3 * mass[i] / 800.0 * np.pi) **(1./3)
        radius[i] = calc
    #print radius
    return radius


########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":


    
    
    
    #################################
    # CLUMPFINDER DATA
    # Extract clumpfinder data
    x_clump, y_clump, mass_clump = extract_ascii_clumpfinder(clumpfile)
    
    # Calculate radius
    radius = radius(mass_clump)



    #############################
    #PARTICLE DATA
    # second subplot
    x_part, y_part = extract_ascii_particles(particlefile)
    xmin=min(x_part)
    ymin=min(y_part)
    xmax=max(x_part)
    ymax=max(y_part)
    centerx=(xmin+xmax)*0.5
    centery=(ymin+ymax)*0.5
    deltax=xmax-xmin
    deltay=ymax-ymin
    borderx=0.01*deltax #will be added to the border of minimal and maximal clump values.
    bordery=0.01*deltay

    while (x_clump[0] + radius[0] > xmax + borderx):
        borderx += 0.1*deltax
    while (x_clump[0] - radius[0] < xmin - borderx):
        borderx += 0.1*deltax
    while (y_clump[0] + radius[0] > ymax + bordery):
        bordery += 0.1*deltay  
    while (y_clump[0] - radius[0] < ymin - bordery):
        bordery += 0.1*deltay       

    deltadomainx=xmax-xmin+2.0*borderx
    deltadomainy=ymax-ymin+2.0*bordery


    if (deltadomainx > deltadomainy):
        coord_start_x=xmin-borderx
        coord_end_x=xmax+borderx
        coord_start_y=centery-deltadomainx*0.5
        coord_end_y=centery+deltadomainx*0.5
    else:
        coord_start_y=ymin-bordery
        coord_end_y=ymax+bordery
        coord_start_x=centerx-deltadomainy*0.5
        coord_end_x=centerx+deltadomainy*0.5
    
    #############################
    #PARTICLE AND CLUMPFINDER DATA
    # third subplot  
    
    
    
    print "Creating figure"

    fig = plt.figure(facecolor='white', figsize=(7,7))
    ax1 = fig.add_subplot(111, aspect='equal', clip_on=True)

    ax1.set_xlim(coord_start_x, coord_end_x)
    ax1.set_ylim(coord_start_y, coord_end_y)   


    #setting up an empty scatterplot for pixel reference
    xedges=[coord_start_x, coord_end_x]
    yedges=[coord_start_y, coord_end_y]
    emptyscatter=ax1.scatter(xedges, yedges, s=0.0)
    ax1.set_xlim(coord_start_x, coord_end_x)
    ax1.set_ylim(coord_start_y, coord_end_y)   

    # Calculating the ratio of pixel-to-unit
    
    upright = ax1.transData.transform((coord_end_x, coord_end_y))
    lowleft = ax1.transData.transform((coord_start_x, coord_start_y))
    x_to_pix_ratio = (upright[0] - lowleft[0])/(coord_end_x-coord_start_x)
    y_to_pix_ratio = (upright[1] - lowleft[1])/(coord_end_y-coord_start_y)

    # Take the mean value of the ratios because why not 
    dist_to_pix_ratio = (x_to_pix_ratio + y_to_pix_ratio) / 2.0
    # Calculate marker size
    clumpsize = np.zeros(len(radius))
    for i in range(0, len(radius)):
        calc = (radius[i]*dist_to_pix_ratio)**2
        clumpsize[i] = calc
        


    ax1.scatter(x_clump, y_clump, s=clumpsize, alpha=0.2, lw=0)
    ax1.scatter(x_clump, y_clump, s=10, alpha=1, lw=0,color='k')
    ax1.scatter(x_part, y_part, s=20, color='red', alpha=0.6, marker=".", lw=0)
    ax1.set_title(title, family='serif')
    ax1.set_xlim(coord_start_x, coord_end_x)
    ax1.set_ylim(coord_start_y, coord_end_y)   






    

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "Saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=600)
    plt.close()

    print "Done", outputfilename+".png"
