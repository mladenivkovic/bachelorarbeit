#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import subprocess
import numpy as np
import matplotlib.pyplot as plt

clumpid=str(argv[1])
noutput=len(argv)-2
outputfilename = "phi_plot_all_log"+clumpid
title='potential profile plot clump '+clumpid
workdir= str(getcwd())


def get_data(filename):
    print ''
    print " Extracting data from", filename

    data=np.loadtxt(filename, dtype='float', skiprows=1)


    # Other useful options:
    #   skiprows=N   skips first N rows
    #   Each row in the text file must have the same number of values.
    return data[:,0], data[:,1]

########################################################################
########################################################################
########################################################################
########################################################################


if __name__ == "__main__":

    print "Creating figure"
    fig = plt.figure(facecolor='white', figsize=(10,16))
    ax1 = fig.add_subplot(111)

  
    for i in range(noutput):
        inputfile=str(argv[i+2])
        dist,phi=get_data(inputfile)
        pot=inputfile[:7]
        style=inputfile[:15]
        style=style[-7:]
        print pot,style, inputfile
        bins=inputfile[-9:]
        bins=bins[:5]
        bins=bins.lstrip("0")
        ax1.loglog(dist,(-1.0)*phi,label=pot+' potential with '+bins+' '+style)
   





    ax1.set_xlabel('distances')
    ax1.set_ylabel('- potential', size=20)
    ax1.set_title(title, family='serif', size=20) 
    ax1.legend(loc=4)



    

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"
