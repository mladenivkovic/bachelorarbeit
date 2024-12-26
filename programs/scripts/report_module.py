# A module for the reportplot* scripts

import numpy as np
from sys import argv #command line arguments
import warnings



##########################
##--- GENERAL VARIABLES ##
##########################


fullcolorlist=['red', 'green', 'blue', 'black', 'magenta', 'lime','cyan','mediumpurple', 'gold','lightpink','lime','saddlebrown','darkolivegreen','cornflowerblue','dimgrey','navajowhite','black','darkslategray','silver','mediumseagreen','orange','midnightblue','silver']













#########################
##--- ACQUIRING DATA   ##
#########################


def get_level_list(noutput):
    for i in range(0,noutput):
        inputfile=str(argv[i+4]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0,1])
        if(temp_data_int.shape[0]>0):
            if 'data_int' in locals():
                data_int= np.vstack((data_int, temp_data_int))
            else:
                data_int = temp_data_int

    
    maxid_clump=max(data_int[:,0]) #how many clumps

    for i in range(0,noutput):
        inputfile=str(argv[i+4+2*noutput]) 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0])
        if(len(np.atleast_1d(temp_data_int))>1):# and temp_data_int.shape[0]>0):
            if 'halo_data' in locals():
                halo_data= np.concatenate((halo_data, temp_data_int))
            else:
                halo_data = temp_data_int

    maxid_halo=max(halo_data) #how many clumps
    clumpnr=max((maxid_halo, maxid_clump))

    levels=np.zeros(clumpnr+1)
    for k in range(len(levels)):
        levels[k]=-2
    

    for j in range(data_int.shape[0]):
        # if data_int[j][0]==data_int[j][2]:
        #     #is halo: set -1
        #     levels[data_int[j][0]]=-1
        # else:
            # is child: set clump level
        levels[data_int[j][0]]=data_int[j][1]

    for k in range(len(halo_data)):
        levels[int(halo_data[k])]=-1

    maxlevel=int(max(levels))
    # return halos,maxlevel,children,child_levels
    return levels, maxlevel




#----------------------------------------------------------

def get_particle_data_level(levels,noutput,particles,maxlevel):
    # for cosmo scripts; find particles of halos from halo list,
    # store them by level
    # READ CLUMP DATA IN FIRST
    print "Reading in particle data"
    data=np.zeros((particles,5))
    particle_index=0
    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6,7])
    
        if (temp_data.shape[0]>0):
            for j in range(temp_data.shape[0]):
                for k in range(5):
                    data[j+particle_index,k]=temp_data[j,k]
        
            particle_index=particle_index+temp_data.shape[0]

    c=0
    for j in range(data.shape[0]):
        if data[j][3]==0:
            c+=1
    print "counting nonbelonging particles ", c

    print data.shape
    print particle_index
    levelind=np.zeros(maxlevel+1)
    x=[]
    y=[]
    z=[]
    for i in range(maxlevel+1):
        x.append(np.zeros(particles))
        y.append(np.zeros(particles))
        z.append(np.zeros(particles))
    
    halox=np.zeros(particles)
    haloy=np.zeros(particles)
    haloz=np.zeros(particles)
    hc=0



    for i in range(data.shape[0]):
        if levels[int(data[i,3])]>=0 :
            lev=int(levels[int(data[i,3])])
            ind=int(levelind[lev])
            x[lev][ind]=(data[i,0])
            y[lev][ind]=(data[i,1])
            z[lev][ind]=(data[i,2])
            levelind[lev]+=1


        elif (levels[int(data[i,3])]==-1):
            # append halo particles 
            halox[hc]=(data[i,0])
            haloy[hc]=(data[i,1])
            haloz[hc]=(data[i,2])
            hc+=1


    print levelind
    print hc

    x_final=[]
    y_final=[]
    z_final=[]
    for i in range(maxlevel+1):
        x_final.append(np.zeros(int(levelind[i])))
        y_final.append(np.zeros(int(levelind[i])))
        z_final.append(np.zeros(int(levelind[i])))
        for j in range(int(levelind[i])):
            x_final[i][j]=x[i][j]
            y_final[i][j]=y[i][j]
            z_final[i][j]=z[i][j]

    halox_final=np.zeros(hc) 
    haloy_final=np.zeros(hc) 
    haloz_final=np.zeros(hc) 

    
    for i in range(hc):
        halox_final[i]=halox[i]
        haloy_final[i]=haloy[i]
        haloz_final[i]=haloz[i]

        


    return x_final,y_final,z_final,halox_final,haloy_final,haloz_final




#==========================================
#==========================================
#==========================================
# get children list
def get_clump_data(halo,noutput):
    print "Reading in clump data."

    children=[]
    child_levels=[]
    
    for i in range(0,noutput):
        inputfile=str(argv[i+4]) 
        
        # get clump center
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[4,5,6])
        if(temp_data.shape[0]>0):
            if 'data' in locals():
                data = np.vstack((data, temp_data))
            else:
                data = temp_data
        
        #get clump ids, parents and levels
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            temp_data_int=np.loadtxt(inputfile, dtype='int', skiprows=1, usecols=[0,1,2])
        if(temp_data_int.shape[0]>0):
            if 'data_int' in locals():
                data_int= np.vstack((data_int, temp_data_int))
            else:
                data_int = temp_data_int


    i=0
    clumpx=0
    clumpy=0
    clumpz=0
    while(i<data_int.shape[0]):
        if (data_int[i,2] in children or data_int[i,2]==halo): #if parent is halo or one of the children
            if (data_int[i,0] != halo):
                if (children.count(data_int[i,0])==0):
                    children.append(data_int[i,0])
                    child_levels.append(data_int[i,1])
                    i=-1
            else:
                clumpx=data[i,0]
                clumpy=data[i,1]
                clumpz=data[i,2]

        i+=1

    # return clumpx, clumpy, clumpz, children
    return children,child_levels,clumpx,clumpy,clumpz



def get_particle_data(children,halo,noutput,particles):
    # READ CLUMP DATA IN FIRST
    print "Reading in particle data"
    data=np.zeros((particles,5))
    particle_index=0
    for i in range(0,noutput):
        inputfile=str(argv[i+4+noutput]) 
        temp_data=np.loadtxt(inputfile, dtype='float', skiprows=1, usecols=[0,1,2,6,7])
    
        if (temp_data.shape[0]>0):
            for j in range(temp_data.shape[0]):
                for k in range(5):
                    data[j+particle_index,k]=temp_data[j,k]
        
            particle_index=particle_index+temp_data.shape[0]-1

    # filter out all non-clump particles
    filteredx=np.zeros(particles) #first guess for length.
    filteredy=np.zeros(particles)
    filteredz=np.zeros(particles)
    clumpid=np.zeros(particles)
    halox=np.zeros(particles)
    haloy=np.zeros(particles)
    haloz=np.zeros(particles)
    unboundx=np.zeros(particles)
    unboundy=np.zeros(particles)
    unboundz=np.zeros(particles)
    unboundclumpid=np.zeros(particles)

    fc=0
    hc=0
    uc=0

    for i in range(data.shape[0]):
        if (len(children)>0):
            # for j in range(0,len(children)):
                # if (data[i,3]==children[j]):
            if (data[i,3] in children):
                filteredx[fc]=data[i,0]  
                filteredy[fc]=data[i,1]
                filteredz[fc]=data[i,2] 
                clumpid[fc]=data[i,3]
                fc+=1

                #get unbound prtcls
                if (data[i,4]>0):
                    unboundx[uc]=data[i,0]
                    unboundy[uc]=data[i,1]
                    unboundz[uc]=data[i,2]
                    unboundclumpid[uc]=data[i,3]
                    uc+=1

        if (data[i,3]==halo):
            # append halo particles 
            halox[hc]=data[i,0]
            haloy[hc]=data[i,1]
            haloz[hc]=data[i,2]
            hc+=1
            
            #get unbound prtcls
            if (data[i,4]>0):
                unboundx[uc]=data[i,0]
                unboundy[uc]=data[i,1]
                unboundz[uc]=data[i,2]
                unboundclumpid[uc]=data[i,3]
                uc+=1


    fx=np.zeros(fc)
    fy=np.zeros(fc)
    fz=np.zeros(fc)
    cid=np.zeros(fc)
    for i in range(fc):
        fx[i]=filteredx[i]
        fy[i]=filteredy[i]
        fz[i]=filteredz[i]
        cid[i]=clumpid[i]

    hx=np.zeros(hc)
    hy=np.zeros(hc)
    hz=np.zeros(hc)
    for i in range(hc):
        hx[i]=halox[i]
        hy[i]=haloy[i]
        hz[i]=haloz[i]

    ux=np.zeros(uc)
    uy=np.zeros(uc)
    uz=np.zeros(uc)
    ucid=np.zeros(uc)
    for i in range(uc):
        ux[i]=unboundx[i]
        uy[i]=unboundy[i]
        uz[i]=unboundz[i]
        ucid[i]=unboundclumpid[i]

    return fx, fy, fz, cid, hx, hy, hz, ux, uy, uz, ucid







#----------------------------------------------------------






def get_level_particles(child_levels,children,ilevel,x_part,y_part,z_part,clumpid):
    x=None
    y=None
    z=None
   
    for i in range(len(children)):
        if (child_levels[i]==ilevel):
            xch,ych,zch=get_child_particles(x_part,y_part,z_part,clumpid,children[i])
            if (xch.shape[0]>0):
                if x is None:
                    x=xch
                    y=ych
                    z=zch
                else:
                    x=np.concatenate((x,xch),axis=0)
                    y=np.concatenate((y,ych))
                    z=np.concatenate((z,zch))
    
    
    return x, y, z










#----------------------------------------------------------





def get_child_particles(x_part,y_part,z_part,clumpid,child):
    xtemp=np.zeros(len(x_part))
    ytemp=np.zeros(len(x_part))
    ztemp=np.zeros(len(x_part))
    counter=0
    for j in range(0,len(x_part)):
        if (clumpid[j]==child):
            xtemp[counter]=x_part[j]
            ytemp[counter]=y_part[j]
            ztemp[counter]=z_part[j]
            counter+=1

    x=np.zeros(counter)
    y=np.zeros(counter)
    z=np.zeros(counter)
    for j in range(counter):
        x[j]=xtemp[j]
        y[j]=ytemp[j]
        z[j]=ztemp[j]
    
    ##########################################
    # print out particles if needed
    #         for j in range(len(x)):
    #             print ('{0:12.7f}{1:12.7f}{2:12.7f}{3:12d}'.format(x[j], y[j], z[j], i+1))
    ##########################################

    return x, y, z






#----------------------------------------------------------







#########################
##--- PLOTTING 2D      ##
#########################

def plot_children2D(children, clumpid, x_part, y_part,z_part,pointsize, pointalpha, toomanychildren, ax1, ax2,ax3):

    # plot children
    if (len(children)>0):
        if (toomanychildren):
            ax1.scatter(x_part,y_part,s=pointsize,c='blue', label='ptcls of child clumps: '+str(len(x_part)), lw=0, marker=',',alpha=pointalpha)
            ax2.scatter(y_part,z_part,s=pointsize,c='blue', label='ptcls of child clumps: '+str(len(x_part)), lw=0, marker=',',alpha=pointalpha)
            ax3.scatter(x_part,z_part,s=pointsize,c='blue', label='ptcls of child clumps: '+str(len(x_part)), lw=0, marker=',',alpha=pointalpha)


        else:
                ax1.scatter(x,y,s=pointsize,c=fullcolorlist[i+1], label='ptcls of child clump '+str(children[i])+':'+str(len(x)), lw=0, marker=',',alpha=pointalpha)
                ax2.scatter(y,z,s=pointsize,c=fullcolorlist[i+1], label='ptcls of child clump '+str(children[i])+':'+str(len(x)), lw=0, marker=',',alpha=pointalpha)
                ax3.scatter(x,z,s=pointsize,c=fullcolorlist[i+1], label='ptcls of child clump '+str(children[i])+':'+str(len(x)), lw=0, marker=',',alpha=pointalpha)
    return






#----------------------------------------------------------


def get_plot_params(x,which,counter,clumpID):
    mylw=0
    mymarker=','


    if (which=='add-to-halo-cos'):
        mylabel=None
        message='halo-namegiver clump'+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=3
        mylw=0.0
        pointalpha=0.6
        mymarker='o'

    elif (which=='halo'):
        mylabel='halo-namegiver particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=.8
        mylw=0.0
        pointalpha=0.2

    if (which=='halo-two'):
        mylabel='halo-namegiver particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=1
        mylw=0.0
        pointalpha=0.2
    
    if (which=='halo-two-phew'):
        mylabel='halo-namegiver particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=1
        mylw=0.0
        pointalpha=0.2

    elif (which=='halo-sub'):
        mylabel='halo-namegiver particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=.2
        mylw=0.0
        pointalpha=0.2

    elif (which=='halo-cos'):
        mylabel='halo-namegiver particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=3
        mylw=0.0
        pointalpha=0.6
        mymarker='o'

    elif (which=='halo-cos-full'):
        mylabel='halo particles'#+str(clumpID)+': '+str(len(x))
        message='halo-namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=3
        mylw=0.0
        pointalpha=0.6
        mymarker='o'

    elif (which=='sub-cos'):
        mylabel='subhalo '+str(counter)+' particles'#+str(clumpid)+':'+str(len(x))
        message='child clump level'+str(counter )+' : plotting '+str(len(x))+' particles'
        pointsize=8
        pointalpha=.9
        mymarker='o'
    

    elif (which=='levels'):
        mylabel='level '+str(counter-1)+' particles'#+str(clumpID)+':'+str(len(x))
        message='child clump level'+str(counter -1)+' : plotting '+str(len(x))+' particles'
        pointsize=1
        pointalpha=.6


    elif (which=='sub-two'):
        mylabel='subhalo particles'#+str(clumpID)+':'+str(len(x))
        message='child clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=2
        pointalpha=.8

    elif (which=='sub-sub'):
        mylabel='subhalo particles'#+str(clumpID)+':'+str(len(x))
        message='child clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=0.3
        pointalpha=.4

    elif (which=='sub-subsub'):
        mylabel='subsubhalo '+str(counter )+' particles'#+str(clumpID)+':'+str(len(x))
        message='child clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
        pointsize=.8
        pointalpha=.8

   
    
    return mylabel, message, pointsize,pointalpha, mymarker, mylw
   
    




def plot_2D(x,y,ax1,which,counter):
  

    mylabel, message, pointsize,pointalpha,mymarker,mylw=get_plot_params(x,which,counter,-1)

    print mylabel, message, pointsize, pointalpha, mylabel, mylw
    print message
    ax1.scatter(x,y,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,alpha=pointalpha) 
    # ax1.scatter(x,y) 

    return






#----------------------------------------------------------







def make_fancy_axes(ax1,ax2,ax3,ax4,clumpx, clumpy, clumpz, x_part, y_part, z_part,twodim):
    #needs clumpx, clumpy,clumpz from get_clump_data()
    #gets corrections for various axes
    print "Calculating plotting domain."
    maxx=0.0
    maxy=0.0
    maxz=0.0
    for i in range(len(x_part)):
        distx=abs(x_part[i]-clumpx)
        if (distx>maxx):
            maxx=distx
        disty=abs(y_part[i]-clumpy)
        if (disty>maxy):
            maxy=disty
        distz=abs(z_part[i]-clumpz)
        if (distz>maxz):
            maxz=distz





    if (twodim):
        if(maxx>=maxy):
            xyc=maxx
        else:
            xyc=maxy
        
        if(maxy>=maxz):
            yzc=maxy
        else:
            yzc=maxz
        
        if(maxx>=maxz):
            xzc=maxx
        else:
            xzc=maxy

        if (xyc>0):
            ax1.set_xlim(clumpx-1.5*xyc, clumpx+1.5*xyc)
            ax1.set_ylim(clumpy-1.5*xyc, clumpy+1.5*xyc)   
        if (yzc>0):
            ax2.set_xlim(clumpy-1.5*yzc, clumpy+1.5*yzc)
            ax2.set_ylim(clumpz-1.5*yzc, clumpz+1.5*yzc)   
        if (xzc>0):
            ax3.set_xlim(clumpx-1.5*xzc, clumpx+1.5*xzc)
            ax3.set_ylim(clumpz-1.5*xzc, clumpz+1.5*xzc)   

    else: # 3-dim
        corr=max((maxx,maxy,maxz))
        if (corr>0):
            ax1.set_xlim(clumpx-1.5*corr, clumpx+1.5*corr)
            ax1.set_ylim(clumpy-1.5*corr, clumpy+1.5*corr)
            ax1.set_zlim(clumpz-1.5*corr, clumpz+1.5*corr)
            ax2.set_xlim(clumpx-1.5*corr, clumpx+1.5*corr)
            ax2.set_ylim(clumpy-1.5*corr, clumpy+1.5*corr)
            ax2.set_zlim(clumpz-1.5*corr, clumpz+1.5*corr)
            ax3.set_xlim(clumpx-1.5*corr, clumpx+1.5*corr)
            ax3.set_ylim(clumpy-1.5*corr, clumpy+1.5*corr)
            ax3.set_zlim(clumpz-1.5*corr, clumpz+1.5*corr)
            ax4.set_xlim(clumpx-1.5*corr, clumpx+1.5*corr)
            ax4.set_ylim(clumpy-1.5*corr, clumpy+1.5*corr)
            ax4.set_zlim(clumpz-1.5*corr, clumpz+1.5*corr)
    return 






#----------------------------------------------------------






def tweak_plot_2D(fig,plt,ax1,case):
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties # for legend
     # print ax1.azim, ax1.elev, ax1.dist

    fontP=FontProperties()
    fontP.set_size('x-large') 
    fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']

    #shift axes
    if (case=='cos'):
        # set tick params (especially digit size)
        ax1.tick_params(axis='both',which='major',labelsize=12,top=5)

        #label axes
        ax1.set_xlabel(r'x', labelpad=15, family='serif',size=16)
        ax1.set_ylabel(r'y', labelpad=15, family='serif',size=16)
        # ax1.set_zlabel(r'kpc', labelpad=15, family='serif',size=16)
        ax1.set_xlim(0,1)
        ax1.set_ylim(0,1)
        plt.subplots_adjust(left=0., right=1, top=1, bottom=0.0,wspace=0.0,hspace=0.0)

    if (case=='mf'):
        ax1.tick_params(axis='both',which='major',labelsize=12,top=5)
        ax1.set_xlabel(r'subclump particles (binned)', labelpad=15, family='serif',size=16)
        ax1.set_ylabel(r'number of subclumps in bin', labelpad=15, family='serif',size=16)
    
        plt.subplots_adjust(left=0.5, right=.95, top=.95, bottom=0.5,wspace=0.0,hspace=0.0)

        fontP.set_size('medium') 
    
    



    #LEGEND


    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=1)
    for l in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[l]._sizes = [20]
        lgnd1.legendHandles[l].set_alpha(1)


#########################
##--- PLOTTING 3D      ##
#########################


def plot_3D(x,y,z,ax1,which,counter,clumpID):

    from mpl_toolkits.mplot3d import Axes3D

    mylabel, message, pointsize,pointalpha, mymarker, mylw=get_plot_params(x,which,counter,-1)

    print message
    ax1.scatter(x,y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)
    return


#----------------------------------------------------------






def tweak_plot_3D(fig,plt, ax1,case):
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import subplots_adjust
    from matplotlib.font_manager import FontProperties # for legend
     # print ax1.azim, ax1.elev, ax1.dist


    # default Legend parameters
    legloc = 0
    legsize = 'x-large'
    bbox=False

    #shift axes
    if (case=='cos'): 
        ax1.view_init(elev=40,azim=40)
        ax1.tick_params(axis='both',which='major',labelsize=18,pad=12)

        ax1.set_xlabel(r'x', labelpad=20, family='serif',size=24)
        ax1.set_ylabel(r'y', labelpad=20, family='serif',size=24)
        ax1.set_zlabel(r'z', labelpad=25, family='serif',size=24)


        # ax1.set_xticklabels(["",-0.015,"","","","","",0.015,""],va='baseline',ha='right')
        # ax1.set_yticklabels(["","0.310","","0.330",""],va='baseline',ha='left')
        # ax1.set_zticklabels(["","0.885","","","","","","0.915",""],va='baseline',ha='left')

        ax1.set_xlim3d(-0.02,0.02)
        ax1.set_ylim3d(0.30,0.35)
        ax1.set_zlim3d(0.880,0.920)
        
        
        ax1.w_xaxis.set_pane_color( (0,0.1,0.7,.15) )
        ax1.w_yaxis.set_pane_color( (0,0.1,0.7,.15) )
        ax1.w_zaxis.set_pane_color( (0,0.1,0.7,.15) )

        ax1.grid()
        ax1.w_xaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_yaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_zaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})

        legloc = 'upper left'
        legsize = 22
        bbox=True
        bbox_to_anchor=(.51, 1.01)

        subplots_adjust(left=-0.01, right=1.01, top=1.00, bottom=-0.01,wspace=0.00,hspace=0.00)




    elif (case=='two'):
        # ax1.view_init(elev=5,azim=-110)
        ax1.view_init(elev=30,azim=290)

        # set tick params (especially digit size)
        ax1.tick_params(axis='both',which='major',labelsize=18,top=5)

        #label axes
        ax1.set_xlabel(r'x $[kpc]$', labelpad=5, family='serif',size=24)
        ax1.set_ylabel(r'y $[kpc]$', labelpad=5, family='serif',size=24)
        ax1.set_zlabel(r'z $[kpc]$', labelpad=5, family='serif',size=24)
        
        ax1.set_xticklabels([0,"","","","",500],va='baseline',ha='right')
        ax1.set_yticklabels([0,"","","","",500],va='baseline',ha='left')
        ax1.set_zticklabels([0,"","","","",500],va='baseline',ha='left')
        ax1.set_xlim3d(0,500)
        ax1.set_ylim3d(0,500)
        ax1.set_zlim3d(0,500)

        ax1.grid()
        ax1.w_xaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_yaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_zaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_xaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_yaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_zaxis.set_pane_color(( 0,0.1,0.7,.15))


        legloc = 'upper left'
        # legsize = 'xx-large'
        legsize = 22

        bbox=True
        subplots_adjust(left=-0.10, right=1.03, top=1.03, bottom=-0.03,wspace=0.00,hspace=0.00)
        # bbox_to_anchor=(0.55, .97)
        bbox_to_anchor=(0.55, 0.98)



    elif (case=='sub'):
        # ax1.view_init(azim=5, elev=15.)
        # ax1.view_init(elev=60,azim=340)
        ax1.view_init(azim=310, elev=160.)

        ax1.set_xlim3d(0,800)
        ax1.set_ylim3d(0,800)
        ax1.set_zlim3d(0,800)

        ax1.grid(True)
        ax1.w_xaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_yaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_zaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_xaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_yaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_zaxis.set_pane_color(( 0,0.1,0.7,.15))




        # set tick params (especially digit size)
        ax1.tick_params(axis='both',which='major',labelsize=18,pad=0)

        #label axes
        ax1.set_xlabel(r'x $[kpc]$', labelpad=2, family='serif',size=24)
        ax1.set_ylabel(r'y $[kpc]$', labelpad=2, family='serif',size=24)
        # ax1.zaxis.set_rotate_label(False)
        ax1.set_zlabel(r'z $[kpc]$', labelpad=5, family='serif',size=24)#,rotation=90)

        ax1.set_xticklabels([0,"","","","","","","",800],va='bottom',ha='left')
        ax1.set_yticklabels([0,"","","","","","","",800],va='baseline',ha='right')
        ax1.set_zticklabels([0,"","","","","","","",800],va='baseline',ha='right')



        legloc = 'upper left'
        legsize = 22

        subplots_adjust(left=-0.03, right=1.03, top=1.02, bottom=0.00,wspace=0.00,hspace=0.00)

        bbox=True
        bbox_to_anchor=(0.52, .23)



    elif (case=='sub-sub'):


        # ax1.view_init(azim=5, elev=15.)
        # ax1.view_init(elev=60,azim=340)
        ax1.view_init(azim=310, elev=160.)

        ax1.set_xlim3d(300,800)
        ax1.set_ylim3d(300,800)
        ax1.set_zlim3d(300,800)

        ax1.grid(True)
        ax1.w_xaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_yaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_zaxis._axinfo.update({'grid' : {'color': (1, 1, 1, 1)}})
        ax1.w_xaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_yaxis.set_pane_color(( 0,0.1,0.7,.15))
        ax1.w_zaxis.set_pane_color(( 0,0.1,0.7,.15))




        # set tick params (especially digit size)
        ax1.tick_params(axis='both',which='major',labelsize=18,pad=0)

        #label axes
        ax1.set_xlabel(r'x $[kpc]$', labelpad=2, family='serif',size=24)
        ax1.set_ylabel(r'y $[kpc]$', labelpad=2, family='serif',size=24)
        # ax1.zaxis.set_rotate_label(False)
        ax1.set_zlabel(r'z $[kpc]$', labelpad=5, family='serif',size=24)#,rotation=90)

        ax1.set_xticklabels([300,"","","","",800],va='bottom',ha='left')
        ax1.set_yticklabels([300,"","","","",800],va='baseline',ha='right')
        ax1.set_zticklabels([300,"","","","",800],va='baseline',ha='right')



        legloc = 'upper left'
        legsize = 22

        subplots_adjust(left=-0.03, right=1.03, top=1.02, bottom=0.00,wspace=0.00,hspace=0.00)

        bbox=True
        bbox_to_anchor=(0.52, .23)



  



    #LEGEND

    fontP=FontProperties()
    fontP.set_size(legsize)
    fontP.set_family('serif') # families = ['serif', 'sans-serif', 'cursive', 'fantasy', 'monospace']
    if bbox:
        lgnd1=ax1.legend(scatterpoints=1,prop=fontP, fancybox=True, framealpha=1, bbox_to_anchor=bbox_to_anchor)
    else:
        lgnd1=ax1.legend(loc=legloc, scatterpoints=1,prop=fontP, fancybox=True, framealpha=1)

    for l in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[l]._sizes = [30]
        lgnd1.legendHandles[l].set_alpha(1)

       


def save_fig(this_name,fig,workdir):
    import matplotlib.pyplot as plt
    fig_path = workdir+'/'+this_name+'.png'
    print "saving figure as "+fig_path
    plt.savefig(fig_path, format='png', facecolor=fig.get_facecolor(), transparent=False, dpi=100)#,bbox_inches='tight' )
    print "done", this_name+'.png'





#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------






#########################
##  NOT USED ANYMORE   ##
#########################



def plot_halo2D(halo,halox,haloy,haloz,ax1,ax2,ax3,pointalpha,pointsize):

    print 'halo namegiver clump '+str(halo)+' : plotting '+str(len(halox))+' particles'
# X-Y PLANE
    ax1.scatter(halox,haloy, s=pointsize, color=fullcolorlist[0], alpha=pointalpha, marker=",", lw=0, label='ptcls of halo-namegiver '+str(halo))

# Y-Z PLANE
    ax2.scatter(haloy,haloz, s=pointsize, color=fullcolorlist[0], alpha=pointalpha, marker=",", lw=0, label='ptcls of halo-namegiver '+str(halo))

# X-Z PLANE
    ax3.scatter(halox,haloz, s=pointsize, color=fullcolorlist[0], alpha=pointalpha, marker=",", lw=0, label='ptcls of halo-namegiver '+str(halo))

    return






#----------------------------------------------------------






def plot_unbounds(unboundx,unboundy,unboundz,ax1,ax2,ax3,pointsize,pointalpha):
    if (len(unboundx)>0):
        print "plotting ", len(unboundx), "unbound particles"
        ax1.scatter(unboundx,unboundy,s=3.0*pointsize,c=fullcolorlist[0], label='unbound ptcls: '+str(len(unboundx)), lw=0.3, marker='o',alpha=pointalpha) 
        ax2.scatter(unboundy,unboundz,s=3.0*pointsize,c=fullcolorlist[0], label='unbound ptcls: '+str(len(unboundx)), lw=0.3, marker='o',alpha=pointalpha) 
        ax3.scatter(unboundx,unboundz,s=3.0*pointsize,c=fullcolorlist[0], label='unbound ptcls: '+str(len(unboundx)), lw=0.3, marker='o',alpha=pointalpha) 
    else:
        print "No unbound particles found."


    return


#----------------------------------------------------------