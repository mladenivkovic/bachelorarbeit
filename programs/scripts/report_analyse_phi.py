#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

# Calculate, analyse and plot the potentials of a subclump in dependance of the number of
# bins used


from os import getcwd
from sys import argv, stderr
import numpy as np
import matplotlib.ticker
import scipy.integrate
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties # for legend

fontP=FontProperties()
fontP.set_size('large') 
fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

clumpid=str(argv[1])
nlin=int(argv[2])
nlog=int(argv[3])
# outputfilename = "phi_semilogx_"+clumpid
outputfilename = "phi_errors_plot_"+clumpid
workdir= str(getcwd())

fullcolorlist=['red', 'green', 'blue', 'gold', 'magenta', 'cyan','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','black','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue','silver']

def get_data(filename):
    # print ''
    # print " Extracting data from", filename

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

    #==================
    # Linear Bins
    #==================


    dist_lin=[]
    phi_lin=[]
    bin_lin=[]

    # print "Reading in data."
    for i in range(nlin):
        inputfile=str(argv[i+4])
        dist,phi=get_data(inputfile)
        dist_lin.append(dist)
        phi_lin.append(phi)
        bin_lin.append(len(phi)-1)


    phi_lin_norm = phi_lin[-1][-1]
    phi_lin_diff=[]
    int_lin=[]
    max_lin=[]

    epsilon=1e-6
    dist_max=len(dist_lin[-1])
    diff_last_lin=np.zeros(len(dist_lin[-1]))
    
    # distlin=np.zeros(12000)
    # di=0


    for i in range(len(dist_lin)):
        size=len(dist_lin[i])
        diff=np.zeros(size)
        ind_ref=0
        for j in range(size):
            d=dist_lin[i][j]
            # ind_orig=ind_ref
            for k in range(ind_ref, dist_max):
                if abs(d-dist_lin[-1][ind_ref])>epsilon*dist_lin[-1][-1]:
                    ind_ref+=1
                else:
                    # distlin[di]=d-dist_lin[-1][ind_ref]
                    # di+=1
                    break

            diff[j] = abs((phi_lin[i][j]-phi_lin[-1][ind_ref])/(phi_lin[-1][ind_ref]))
        
        phi_lin_diff.append(diff)
        # integ=scipy.integrate.trapz(phi_lin[i],dist_lin[i])
        # int_lin.append(integ)
        max_lin.append(max(diff))


    ratio_lin2=[]
    ratio_lininf=[]
    # ratio_linint=[]
    for i in range(len(max_lin)):
        totdiff = 0
        for j in phi_lin_diff[i]:
            totdiff += j*j
        totdiff = np.sqrt(totdiff/len(phi_lin_diff[i]))
        ratio_lin2.append(totdiff)
        ratio_lininf.append(max_lin[i])
        # ratio_linint.append(float(int_lin[-1]-int_lin[i])/int_lin[-1])


#     print ""
    # print ('{0:<14}{1:^8}{2:<14}{1:^8}{3:<14}'.format('Bins',"&", 'L$_2$ Lin', 'L$_\infty$ Lin'))
    # for i in range(len(int_lin)):
    #     print ('{0:14d}{1:^8}{2:14.4f}{1:^8}{3:14.4f}'.format(bin_lin[i], "&", ratio_lin2[i], ratio_lininf[i] ))
    # 
    # 
    # print "============================================================================="






    #==================
    # Logarithmic Bins
    #==================
    dist_log=[]
    phi_log=[]
    bin_log=[]
    for i in range(nlog):
        inputfile=str(argv[i+4+nlog])
        dist,phi=get_data(inputfile)
        dist_log.append(dist)
        phi_log.append(phi)
        bin_log.append(len(phi)-1)


    phi_log_norm = phi_log[-1][-1]
    phi_log_diff=[]
    int_log=[]
    max_log=[]

    epsilon=1e-6
    dist_max=len(dist_log[-1])
    diff_last_log=np.zeros(len(dist_log[-1]))

    # distlog=np.zeros(12000)
    # di=0

    for i in range(len(dist_log)):
        size=len(dist_log[i])
        diff=np.zeros(size)
        ind_ref=0
        for j in range(size):
            d=dist_log[i][j]
            # ind_orig=ind_ref
            for k in range(ind_ref, dist_max):
                if abs(d-dist_log[-1][ind_ref])>epsilon*dist_log[-1][-1]:
                    ind_ref+=1
                else:
                    break

            diff[j] = abs((phi_log[i][j]-phi_log[-1][ind_ref])/phi_log[-1][ind_ref])
        
        phi_log_diff.append(diff)
        # integ=scipy.integrate.trapz(phi_log[i],dist_log[i])
        # int_log.append(integ)
        max_log.append(max(diff))


    # print max(distlog)
    ratio_log2=[]
    ratio_loginf=[]
    ratio_logint=[]
    for i in range(len(max_log)):
        totdiff = 0
        for j in phi_log_diff[i]:
            totdiff += j*j
        totdiff = np.sqrt(totdiff/len(phi_log_diff[i]))
        ratio_log2.append(totdiff)
        ratio_loginf.append(max_log[i])
        # ratio_logint.append(float(int_log[-1]-int_log[i])/int_log[-1])


      
    for i in range(3):
        print
    
    print "TABLE: || phi[bins] - phi[10'000]|| / || phi[10'000] ||"
    print
    print "L2 norm:   [ 1/N sum (phi[bins][i] - phi[10000][i])^2 ] ^ 1/2"
    print "L_inf norm: max{abs(phi[bins][i] - phi[10000][i])^2)} "
    print
    #only works if there are the same bins

    #=========================
    # Print with integrals
    #=========================
    # print ('{0:<12}{1:^8}{2:<12}{1:^8}{3:<12}{1:^8}{4:<12}{1:^8}{5:<12}{1:^8}{6:<12}{1:^8}{7:<12}{8:>4}'.format('Bins',"&", 'L$_2$ Log' ,'L$_\infty$ Log', 'Int$_{log}$', 'L$_2$ Lin', 'L$_\infty$ Lin', 'Int$_{lin}$','\\\\'))
    # for i in range(len(int_log)):
    #     print ('{0:12d}{1:^8}{2:12.4f}{1:^8}{3:12.4f}{1:^8}{4:12.4f}{1:^8}{5:12.4f}{1:^8}{6:12.4f}{1:^8}{7:12.4f}{8:>4}'.format(bin_log[i], "&", ratio_log2[i], ratio_loginf[i], ratio_logint[i], ratio_lin2[i], ratio_lininf[i],ratio_linint[i], "\\\\" ))
    


    #=========================
    # Print without integrals
    #=========================

    print ('{0:<14}{1:^8}{2:<14}{1:^8}{3:<14}{1:^8}{4:<14}{1:^8}{5:<14}{6:>4}'.format('Bins',"&", 'L$_2$ Log' ,'L$_\infty$ Log', 'L$_2$ Lin', 'L$_\infty$ Lin','\\\\'))
    for i in range(len(max_log)):
        print ('{0:14d}{1:^8}{2:14.4f}{1:^8}{3:14.4f}{1:^8}{4:14.4f}{1:^8}{5:14.4f}{6:>4}'.format(bin_log[i], "&", ratio_log2[i], ratio_loginf[i], ratio_lin2[i], ratio_lininf[i], "\\\\" ))
    
   







#=============================
# Plot it
# =============================




print >> stderr,"done with the calculations and the table. creating image."
    
fig = plt.figure(facecolor='white', figsize=(8,7))
ax1 = fig.add_subplot(111)



#Plotting
ax1.plot(bin_lin[:-1],ratio_lin2[:-1],'r--',label=r'linear binning, $\sigma_N$')
ax1.plot(bin_lin[:-1],ratio_lininf[:-1],'r',label=r'linear binning, $D_{max,N}$')
ax1.plot(bin_log[:-1],ratio_log2[:-1],'b--',label=r'logarithmic binning, $\sigma_N$')
ax1.plot(bin_log[:-1],ratio_loginf[:-1],'b',label=r'logarithmic binning, $D_{max,N}$')

ax1.plot(bin_lin,ratio_lin2,'ro')
ax1.plot(bin_lin,ratio_lininf,'ro')
ax1.plot(bin_log,ratio_log2,'bo')
ax1.plot(bin_log,ratio_loginf,'bo')



#set axes
ax1.set_xlim(9,1091)

ax1.set_xscale('log')
ax1.set_xticks([10,20,50,100,500,1000])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax1.set_yscale('log')


#grid
ax1.yaxis.grid(True, which='major')
ax1.xaxis.grid(True, which='major')




#Labels and legends
ax1.set_xlabel(r'Number of bins used $N$', family='serif', size=20)
ax1.set_ylabel(r'Deviations', family='serif', size=20)

lgnd1=ax1.legend(loc='lower left', prop=fontP, framealpha=0.6)




#Adjustments
plt.subplots_adjust(left=-0.0, right=1.0, top=1.0, bottom=-0.0,wspace=0.00,hspace=0.05)
fig.tight_layout()



#Save fig
workdir= str(getcwd())

fig_path = workdir+'/'+outputfilename+'.png'
# print "saving figure as"+fig_path
plt.savefig(fig_path, format='png', transparent=False, dpi=100,bbox_inches='tight')
plt.close()

print >> stderr,"done", outputfilename+".png"
