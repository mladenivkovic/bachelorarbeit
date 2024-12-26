#!/usr/bin/env python

from os import getcwd, chdir
from os.path import exists
import subprocess
from numpy import array
from matplotlib import pyplot
from matplotlib.colors import LogNorm
import multiprocessing as mp

def extract_bin(filename):
    """
    Extract data from a single output file with out_step and mpi_task as input
    Not finished...
    """
    import fortranfile
    filepath = getcwd()+filename
    # open fortran unformatted file
    f = fortranfile.FortranFile(filepath)
    ijminmax = f.readReals()
    dat2 = f.readReals()
    data_map = f.readReals()
    f.close()

    print ijminmax
    print dat2
    print data_map
    return data_map


def extract_ascii(filename):
    """
    Extract the ramses map data from an ascii file
    """
    # First line of file gives map dimensions nx, ny
    awk_callwindow = ['awk', 'NR==1{print $1; print $2}', getcwd()+'/'+filename]
    p1 = subprocess.Popen(awk_callwindow, stdout=subprocess.PIPE)
    stdout_val = p1.communicate()[0]
    p1.stdout.close()
    [nx, ny] = list(map(int, stdout_val.split()))
    # extract map data with awk
    awk_callmap = ['awk', ' {print $3} ', getcwd()+'/'+filename]
    p2 = subprocess.Popen(awk_callmap, stdout=subprocess.PIPE)
    stdout_val = p2.communicate()[0]
    p2.stdout.close()
    data_map = list(map(float, stdout_val.split()))
    # reshape data for imshow
    data_map = array(data_map)
    data_map = data_map.reshape(ny+1, nx+1)
    return data_map


def extract_sink(filename):
    """
    Extract sink positions (and masses) of a file
    """
    awk_callsink = ['awk', '{print $2; print $3; print $4; print $5}', getcwd()+'/'+filename]
    p = subprocess.Popen(awk_callsink, stdout=subprocess.PIPE)
    stdout_val = p.communicate()[0]
    p.stdout.close()
    data = stdout_val.split(",\n")
    data = data[:-1]
    data = list(map(float, data))
    # reshape data to list of list of sinks
    data = array(data)
    data = data.reshape(len(data)/4, 4)
    return data


def sink2map(sink_list, window_centre, window_length, nx, ny):
    """
    Map the sink positions from the box coordinates to the map coordinates
    Find parameters in the amrmapper.sh program
    window_centre -> WINDOW_CENTRE
    window_length -> WINDOW_LENGTH
    """
    x = (sink_list[1]-window_centre)/(window_length/2)*nx*0.5+nx*0.5
    y = (sink_list[2]-window_centre)/(window_length/2)*ny*0.5+ny*0.5
    return x, y


def map_plot(data, fig_name, plotmin=None, plotmax=None, sink_pos=None):
    """
    Plot extracted data
    """
    fig = pyplot.figure(facecolor='black')
    ax = fig.add_subplot(1,1,1)
    ax.axis([0, 500, 0, 500])
    # search min/max for colorbar
    if (plotmin==None): plotmin = data.min()
    if (plotmax==None): plotmax = data.max()
    # plot map
    ax.imshow(data, interpolation='None', cmap='bone', norm=LogNorm(vmin=plotmin, vmax=plotmax))
    ax.tick_params(bottom='off', top='off', left='off', right='off')
    ax.tick_params(labelbottom='off', labeltop='off', labelleft='off', labelright='off')
    # plot sinks
    if (sink_pos==None): print "no sinks found"
    else:
        for s in sink_pos:
            # rotate positions
            x, y = sink2map(s, 0.5, 0.15, 500, 500)
            # plot positions
            ax.scatter(x, y, marker='o', c='white', s=50)
    # save map
    fig_path = getcwd()+'/'+fig_name
    print "saving "+fig_path
    pyplot.savefig(fig_path, facecolor=fig.get_facecolor(), transparent=True, dpi=100)
    pyplot.close()


def map_all(var, path=None):
    """
    Plot all the data of var (e.g. dens) in given path
    """
    # check given path
    if(path==None): path = getcwd()#; print path
    elif((path[0]!="/") and (exists(getcwd()+"/"+path)==True)): path = getcwd()+"/"+path#; print path
    # change working directory
    chdir(path)
    print getcwd()
    # search all files
    grep_call = "ls | grep "+var#+" | awk '{for(x=1;x<=NF;x++)a[++y]=$x}END{c=asort(a); print a[c];}' | cut -d'_' -f2 | cut -d'.' -f1"
    p = subprocess.Popen(grep_call, shell=True, stdout=subprocess.PIPE)
    files = p.communicate()[0].split()
    p.stdout.close()
    # search all sink_files
    grep_call = "ls | grep sink"
    p = subprocess.Popen(grep_call, shell=True, stdout=subprocess.PIPE)
    sink_files = p.communicate()[0].split()
    p.stdout.close()
    # get min/max for consistent colorbar
    data = extract_ascii(files[-1])
    min_val = data.min()
    #min_val -= min_val*0.1
    max_val = data.max()
    # plot all the files
     #pool = mp.Pool(processes=4)
     #results = [pool.apply(loop_plotter, args=(f, min_val, max_val)) for f in files]
    for i in range(len(files)):
        data = extract_ascii(files[i])
        sinks = extract_sink(sink_files[i])
        file_id = files[i].split('.')[0].split('_')[-1]
        map_plot(data, "test_"+file_id+".png", min_val, max_val, sink_pos=sinks)
    

def loop_plotter(file_name, min_val, max_val):
    """
    Helper function for muliprocessing map_all
    """
    data = extract_ascii(file_name)
    file_id = file_name.split('.')[0].split('_')[-1]
    map_plot(data, "test_"+file_id+".png", min_val, max_val)



if __name__=="__main__":
    # TODO: add parser, sinks
    #data = extract_ascii("map_data/dens_00100.map")
    #sinks = extract_sink("map_data/sink_00100.csv")
    #map_plot(data, "sink_test_00100.png", sink_pos=sinks)
    map_all(var='dens', path='map_data')
    
