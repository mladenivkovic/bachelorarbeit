#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# This script is called by report_phiplot
# Creates plots with linear axes

from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend
import scipy.integrate
import matplotlib.ticker

fontP=FontProperties()
# fontP.set_size('small') 
fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']
fontP.set_size('x-large')

clumpid=str(argv[1])
# noutput=len(argv)-2
nlin=int(argv[2])
nlog=int(argv[3])
outputfilename = "phi_plot_"+clumpid+"_log"
workdir= str(getcwd())

fullcolorlist=['red', 'green', 'blue', 'gold', 'magenta', 'cyan','black','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','black','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue','silver']

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
    fig = plt.figure(facecolor='white', figsize=(10,7))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)


    print "Plotting Mass Profile"
    for i in range(nlin):
        inputfile=str(argv[i+4])
        print "LIN", inputfile
        dist,phi=get_data(inputfile)
        ax1.semilogx(dist/dist[-1],phi/phi[-1],label=str(len(phi)-1)+'  mass bins',c=fullcolorlist[i])

    for i in range(nlog):
        inputfile=str(argv[i+4+nlin])
        print "LOG", inputfile
        dist,phi=get_data(inputfile)
        ax2.semilogx(dist/dist[-1],phi/phi[-1],label=str(len(phi)-1)+' mass bins',c=fullcolorlist[i])


    # loglog
    # ax1.set_xlim(0.001,1.2)
    # ax1.set_ylim(0.00001,1.2)

    # ax1.set_xlim(0.0,1.1)
    # ax1.set_ylim(0.8,12.1)
    # ax2.set_xlim(0.0,1.1)
    # ax2.set_ylim(0.8,12.1)

    ax1.grid()
    ax2.grid()

    ax1.set_xlabel(r'distances $[r_{max}]$', family='serif', size=20)
    ax1.set_ylabel(r'potential $[\phi(r_{max})]$', family='serif', size=20)
    ax1.set_title('Linear Binning Distances', family='serif', size=22,y=1.05)


    ax2.set_xlabel(r'distances $[r_{max}]$', family='serif', size=20)
    ax2.set_ylabel(r'potential $[\phi(r_{max})]$', family='serif', size=20)
    ax2.set_title('Logarithmic Binning Distances', family='serif', size=22,y=1.05) 



    lgnd1=ax1.legend(loc=0, prop=fontP,ncol=2)#, framealpha=0.5)
    lgnd2=ax2.legend(loc=0, prop=fontP,ncol=2)#, framealpha=0.5)
   
    plt.subplots_adjust(left=-0.0, right=1.0, top=1.0, bottom=-0.0,wspace=0.00,hspace=0.05)
    fig.tight_layout()

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=100,bbox_inches='tight')
    plt.close()

    print "done", outputfilename+".png"
