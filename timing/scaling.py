import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
#from cycler import cycler

import Timing as timing
import Extractor as extractor

# timings to plot
timings = ['mainTimer',
           'AMR AssignDensity',
           'AMR sort particles',
           'AMR update particle',
           'Integration',
           'SelfField total',
           'SF: Potential',
           'Boundingbox'
           ]


def collect(dictionary, prop):
    """
    Read out the property prop from a dictionary
        
    Returns
    -------
    a dictionary of the form:
        {name: time}
        
    where "name" is the timing name.
    """
    tmp = {}
    for dic in dictionary:
            if 'main' in dic['what']:
                tmp[ dic['what'] ] = dic['cpu tot']
            else:
                tmp[ dic['what'] ] = dic[prop]
        
    return tmp

def reorder(data):
    """
    Reorder data in order to plot
    use timing names as keys of lists
        
    Returns
    -------
    reordered data where each key has a list of values
    a value is the timing for a specific number of processes
    """
    newdata = {}
    for key in data[0]:
        if key in timings:
            newdata[key] = []
        
    for d in data:
        for key, value in d.iteritems():
            if key in timings:
                newdata[key].append(value)
        
    return newdata


def plot(time, nCores, cmap_name = 'terrain'):
    fig = plt.figure(figsize=(10, 10))
    legends = []

    # 14. July 2017
    # https://stackoverflow.com/questions/8389636/creating-over-20-unique-legend-colors-using-matplotlib
    ax = plt.subplot(111)
    cmap = plt.get_cmap(cmap_name)
    nColors = len(time)
    
 #   ax.set_prop_cycle(cycler('color', [cmap(1.*i/nColors) for i in range(nColors)]))
    ax.set_color_cycle([cmap(1.*i/nColors) for i in range(nColors)])
    i = 0
    
    # 14. July 2017
    # https://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list
    order = sorted(range(len(nCores)), key=lambda k: float(nCores[k]))
    
    nCores_sorted = []
    for o in order:
        nCores_sorted.append(nCores[o]) 
    
    # 14. July 2017
    # https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    for key in time:
        
        times_sorted = []
        for o in order:
            times_sorted.append(time[key][o])
        
        ax.semilogy(nCores_sorted, times_sorted, linewidth=3) #, color=colors[i])
        legends.append(key)
            
        i += 1
        
    #plt.xlim([int(nCores[0]), int(nCores[-1])+2])
    #plt.ylim([int(nCores[0]), int(nCores[-1])+2])

    ax.legend(legends, loc='upper left', bbox_to_anchor=(1.0, 1.0))
    plt.xlabel('#cores', fontsize=18)
    plt.xticks(fontsize=16)
    plt.ylabel('time [s]', fontsize=18)
    plt.yticks(fontsize=16)
    plt.grid()
    plt.show()


try:

    parser = argparse.ArgumentParser(description='Create a scaling plot')
    parser.add_argument('--directory',
                        help='Directory to OPAL output files',
                        default="./",
                        type=str)
    parser.add_argument('--extension',
                        help="File exenstion of output files.\n" + \
                             "E.g. '.o259*' allows to find all files\n" + \
                             "that contain '.o259' in the extension",
                         type=str)
    
    args = parser.parse_args()
    
    directory = args.directory
    extension = args.extension
    
    theExtractor = extractor.Extractor()
    
    theExtractor.collect(ext = extension, path = directory)
    
    files = theExtractor.getFiles()
    
    # a list of times per core
    time = []
    cores = []
    for f in files:
        data = theExtractor.extract(f)
        cores.append( data[0]['cores'] )
        time.append( collect(data, 'cpu avg') )
        
    time = reorder(time)
    
    plot(time, cores)
    
    
except Exception as e:
    print( e )
    
