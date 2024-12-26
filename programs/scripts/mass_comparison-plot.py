#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script will create a figure containing 2 histograms:
# One is the particle-sum mass of a clump, the other is the
# clump mass calculated by ramses for each relevant peak.

# Usage: execute the corresponding bash script.

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt

filename=str(argv[1])
outputfilename = "mass_comparison_plot"
title='Mass comparison'
workdir= str(getcwd())


def extract_ascii(filename):
    # Extract the necessary data from mladen_masscomparison.txt file.

    print "extracting clumpfinder data"
    # Extract peak ids
    awk_callmap = ['awk', ' NR > 1 { print $1 } ', getcwd()+'/'+filename]
    p1 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p1.communicate()[0]
    p1.stdout.close()
    global_peak_id = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    global_peak_id = np.array(global_peak_id)

    # Extract (sum particle mass) / clump mass
    awk_callmap = ['awk', ' NR > 1 { print $4 } ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    ratio_unitless = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
    ratio_unitless = np.array(ratio_unitless)

#    # Extract (sum particle mass / clump mass ) * particle mass ^-1
#    awk_callmap = ['awk', ' NR > 1 {print $5} ', getcwd()+'/'+filename]
#    p3 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
#    stdout_val = p3.communicate()[0]
#    p3.stdout.close()
#    ratio_in_pm = list(map(float, stdout_val.split())) #eingelesene Strings in Floats umwandeln
#    ratio_in_pm = np.array(ratio_in_pm) 
    
    print "clumpfind data imported"
    return global_peak_id, ratio_unitless#, ratio_in_pm




########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    print "Creating figure"
   
    #################################
    # Extract data
#    ids, ratio, ratio_mp = extract_ascii(filename)
    ids, ratio = extract_ascii(filename)

    # transform NaN to zeros
    print "Transforming NaNs to zeros"
    for i in range(0, len(ids)):
        if np.isnan(ratio[i]):
            ratio[i] = 0.0
#            ratio_mp[i] = 0.0


    fig = plt.figure(facecolor='white', figsize=(10,16))
    fig.suptitle(title, family='serif', size=20) 
    ax1 = fig.add_subplot(111)
    #ax2 = fig.add_subplot(212)

    ax1.plot(ids, ratio)
    ax1.set_xlabel('global clump index')
    ax1.set_ylabel(r'$\frac{sum\ of\ particle\ masses}{clump\ mass}$', size=20)
    ax1.set_title('Ratio of sum of particle masses over clump mass')

    #ax2.plot(ids, ratio_mp*1e-5)
    #ax2.set_xlabel('global clump index')
    #ax2.set_ylabel(r'$\frac{sum\ of\ particle\ masses}{clump\ mass} \ \cdot 10^{5} (particle\ mass) ^{-1}$', size=20)
    #ax2.set_title('Ratio of sum of particle masses over clump mass per single particle mass')


    

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"
