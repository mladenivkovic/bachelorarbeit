import numpy as np
from sys import argv #command line arguments
import warnings



##########################
##--- GENERAL VARIABLES ##
##########################


fullcolorlist=['red', 'green', 'blue', 'gold', 'magenta', 'cyan','lime','saddlebrown','darkolivegreen','cornflowerblue','orange','dimgrey','navajowhite','black','darkslategray','mediumpurple','lightpink','mediumseagreen','maroon','midnightblue','silver']













#########################
##--- ACQUIRING DATA   ##
#########################





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




#----------------------------------------------------------




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




#--------------------------------------------------------------------------------




def is_child_interesting(clumpid,child):

    # Check whether a clump is interesting to us

    counter=0
    interesting=False
    for j in range(0,len(clumpid)):
        if (clumpid[j]==child):
            counter+=1
            if counter>10 :
                interesting=True
                break

    
    ##########################################
    # print out particles if needed
    #         for j in range(len(x)):
    #             print ('{0:12.7f}{1:12.7f}{2:12.7f}{3:12d}'.format(x[j], y[j], z[j], i+1))
    ##########################################

    return interesting




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


def get_plot_params(x,y,z,pointsize,which,counter,clumpID):
    mylw=0
    mymarker=','
    if (which=='unbound'):
        mylabel='unbound ptcls assigned to '+str(clumpID)+': '+str(len(x))
        message="plotting "+str(len(x))+" unbound particles of clump "+str(clumpID)
        pointsize=3*pointsize
        mylw=0.2
        mymarker='o'

    elif (which=='halo'):
        mylabel='ptcls of halo-namegiver '+str(clumpID)+': '+str(len(x))
        message='halo namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
    
    elif (which=='clump'):
        mylabel='ptcls of clump '+str(clumpID)+': '+str(len(x))
        message='clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'


    elif (which=='children'):
        mylabel='ptcls of child clump '+str(clumpID)+':'+str(len(x))
        message='child clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'

    elif (which=='levels'):
        mylabel="level "+str(counter-1)+' substructure ptcls :'+str(len(x))
        message='substructure particles level '+str(counter-1)+': plotting '+str(len(x))+' particles'  
    
    elif (which=='unblev'):
        mylabel='unbound ptcls assigned to level '+str(counter)+': '+str(len(x))
        message="plotting "+str(len(x))+" unbound particles"
        pointsize=3*pointsize
        mylw=0.2
        mymarker='o'

    elif (which=='COM'):
        mylabel='Center of Mass '+str(clumpID)
        message='Plotting CoM of clump '+str(clumpID)
        pointsize=5*pointsize
        mymarker="s"
        mylw=0.2

    elif (which=='border'):
        mylabel='Closest Border to CoM of '+str(clumpID)
        message='Plotting border of clump '+str(clumpID)
        pointsize=10*pointsize
        mymarker="o"
        mylw=.2

    elif (which=='subhalo'):
        mylabel='ptcls of subhalo '+str(clumpID)+': '+str(len(x))
        message='halo namegiver clump '+str(clumpID)+' : plotting '+str(len(x))+' particles'
   
    return mylabel, message, pointsize, mymarker, mylw



def plot_2D(x,y,z,ax1,ax2,ax3,pointsize,pointalpha,which,counter,clumpID):
  

    mylabel, message, pointsize, mymarker, mylw=get_plot_params(x,y,z,pointsize,which,counter,clumpID)


    print message
    ax1.scatter(x,y,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,alpha=pointalpha) 
    ax2.scatter(y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,alpha=pointalpha) 
    ax3.scatter(x,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,alpha=pointalpha) 


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






def tweak_plot_2D(fig,ax1,ax2,ax3,fontP):
    # SET TITLES AND LABEL AXES

    ax1.set_title("x-y plane", family='serif')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax2.set_title("y-z plane", family='serif')
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    ax3.set_title("x-z plane", family='serif')
    ax3.set_xlabel('x')
    ax3.set_ylabel('z')

    # SET LEGEND
    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    unbc=0
   
   
    for l in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[l]._sizes = [20]
        lgnd2.legendHandles[l]._sizes = [20]
        lgnd3.legendHandles[l]._sizes = [20]
        
       

    fig.tight_layout()


#########################
##--- PLOTTING 3D      ##
#########################


def plot_3D(x,y,z,ax1,ax2,ax3,ax4,pointsize,pointalpha,which,counter,clumpID):

    from mpl_toolkits.mplot3d import Axes3D

    mylabel, message, pointsize, mymarker, mylw=get_plot_params(x,y,z,pointsize,which,counter,clumpID)



    ax1.scatter(x,y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)
    ax2.scatter(x,y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)
    ax3.scatter(x,y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)
    ax4.scatter(x,y,z,s=pointsize,c=fullcolorlist[counter], label=mylabel, lw=mylw, marker=mymarker,depthshade=True,alpha=pointalpha)
    
    
    
    
    return


#----------------------------------------------------------






def tweak_plot_3D(fig, ax1,ax2,ax3,ax4,fontP):
    import matplotlib
     # print ax1.azim, ax1.elev, ax1.dist

    #shift axes
    ax1.view_init(elev=15.,azim=-60)
    ax2.view_init(elev=15.,azim=120)
    ax3.view_init(elev=105., azim=-60)
    ax4.view_init(elev=-75., azim=-60)

    # set tick params (especially digit size)
    ax1.tick_params(axis='both',which='major',labelsize=5)
    ax2.tick_params(axis='both',which='major',labelsize=5)
    ax3.tick_params(axis='both',which='major',labelsize=5)
    ax4.tick_params(axis='both',which='major',labelsize=5)

    #label axes
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('z')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_zlabel('z')
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_zlabel('z')



    #LEGEND

    lgnd1=ax1.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd2=ax2.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd3=ax3.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    lgnd4=ax4.legend(loc=0, scatterpoints=1,prop=fontP, framealpha=0.5)
    for l in range(len(lgnd1.legendHandles)):
        lgnd1.legendHandles[l]._sizes = [20]
        lgnd2.legendHandles[l]._sizes = [20]
        lgnd3.legendHandles[l]._sizes = [20]
        lgnd4.legendHandles[l]._sizes = [20]
        
    matplotlib.pyplot.subplots_adjust(left=0.01, right=0.99, top=0.9, bottom=0.02,wspace=0.05)
       



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
