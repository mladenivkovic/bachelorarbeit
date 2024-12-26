#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox


from os import getcwd
from sys import argv #command line arguments
import matplotlib 
matplotlib.use('Agg') #don't show anything unless I ask you to. So no need to get graphical all over ssh.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend

fontP=FontProperties()
# fontP.set_size('small') 
fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

clumpid=str(argv[1])
# noutput=len(argv)-2
nlin=int(argv[2])
nlog=int(argv[3])
outputfilename = "cmp_plot_"+clumpid
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
    fig = plt.figure(facecolor='white', figsize=(16,10))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)



    print "Plotting Mass Profile"
    for i in range(nlin):
        inputfile=str(argv[i+4])
        print "LIN", inputfile
        dist,cmp=get_data(inputfile)
        ax1.plot(dist/dist[-1],cmp/cmp[-1],label=str(len(cmp)-1)+'  mass bins')
        # ax1.loglog(dist/dist[-1],cmp/cmp[-1],label=str(len(cmp)-1)+'  mass bins')
   

    for i in range(nlog):
        inputfile=str(argv[i+4+nlin])
        print "LOG", inputfile
        dist,cmp=get_data(inputfile)
        ax2.plot(dist/dist[-1],cmp/cmp[-1],label=str(len(cmp)-1)+' mass bins')


    # loglog
    # ax1.set_xlim(0.001,1.2)
    # ax1.set_ylim(0.00001,1.2)
    ax1.set_xlim(-0.1,1.2)
    ax1.set_ylim(-0.1,1.2)
    ax2.set_xlim(-0.1,1.2)
    ax2.set_ylim(-0.1,1.2)

    ax1.set_xlabel(r'distances $[r_{max}]$', family='serif', size=16)
    ax1.set_ylabel(r'cumulative mass $[M_{tot}]$', family='serif', size=16)
    ax1.set_title('Linear Binning Distances', family='serif', size=20) 


    ax2.set_xlabel(r'distances $[r_{max}]$', family='serif', size=16)
    ax2.set_ylabel(r'cumulative mass $[M_{tot}]$', family='serif', size=16)
    ax2.set_title('Logarithmic Binning Distances', family='serif', size=20) 



    lgnd1=ax1.legend(loc=0, prop=fontP, framealpha=0.5)
    lgnd2=ax2.legend(loc=0, prop=fontP, framealpha=0.5)
   
    fig.tight_layout()

    print "Figure created"
    
    
    # saving figure
    fig_path = workdir+'/'+outputfilename+'.png'
    print "saving figure as"+fig_path
    plt.savefig(fig_path, format='png', transparent=False, dpi=300)
    plt.close()

    print "done", outputfilename+".png"
