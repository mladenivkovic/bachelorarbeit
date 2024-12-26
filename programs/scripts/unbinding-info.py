#!/usr/bin/python
##!/zbox/opt/Enthought/Canopy_64bit/User/bin/python # for zbox

import os
import unbinding_module as m
from sys import argv #command line arguments
import warnings





noutput=int(argv[1])
halo=int(argv[2])
particles=int(argv[3])

p=os.getcwd()
head, bins = os.path.split(p)
head2, potential= os.path.split(head)

filename="info_"+potential+"_"+bins+".txt"

children,child_levels,clumpx,clumpy,clumpz=m.get_clump_data(halo,noutput)
x_part,y_part,z_part,clumpid,halox,haloy,haloz,unboundx,unboundy, unboundz,uclid = m.get_particle_data(children,halo,noutput,particles)


f=open(filename,'w')

f.write ('{0:12}{1:12}{2:12}'.format("Info for ",potential, bins))
f.write("\n") 
f.write("\n") 

f.write ('{0:40}{1:10}'.format("halo namegiver ptcls:", len(halox)))
f.write("\n") 

for i in range(0, len(children)):
    x,y,z=m.get_child_particles(x_part,y_part,z_part,clumpid,children[i])
    if len(x)>0:
        f.write ('{0:12}{1:10}{2:18}{3:10}'.format("child clump ",children[i] ," ptcls:", len(x)))
        f.write("\n") 


if (len(unboundx)>0): 
    for i in range(len(children)):
        xu=None
        yu=None
        zu=None
        xu,yu,zu=m.get_child_particles(unboundx,unboundy,unboundz,uclid,children[i])
        if len(xu)>0:
            f.write('{0:28}{1:9}{2:3}{3:10}'.format("unbd ptcls assigned to child", children[i],":", len(xu)))
            f.write("\n") 
        # else:
        #     print "Found no unbound particles assigned to child "+str(children[i])
    xu=None
    yu=None
    zu=None
    xu,yu,zu=m.get_child_particles(unboundx,unboundy,unboundz,uclid,halo)
    if len(xu)>0:
        f.write ('{0:40}{1:10}'.format("unbd ptcls assigned to namegiver:", len(xu)))
        f.write("\n") 
    else:
        f.write ("Found no unbound particles assigned to halo-namegiver "+str(halo))
        f.write("\n") 

else:
    f.write("No unbound particles found.")
    f.write("\n") 

f.close()

print "Done writing info."

