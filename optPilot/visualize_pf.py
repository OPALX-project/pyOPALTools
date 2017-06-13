import os
import sys
import glob
import json
import math

import numpy as np
import pylab as pl

import matplotlib.cm     as cm
import matplotlib.pyplot as plt
#import matplotlib.mlab   as mlab
#from   matplotlib.backends.backend_pdf import PdfPages
from collections import OrderedDict

from Annotate import AnnoteFinder


# Data parsing
##############################################################################

# name of the columns in the solution data
nameToColumnMap = {}

def buildNameToColumnMapJSON(filename):
    data = json.load(open(filename), object_pairs_hook=OrderedDict)

    for idx, name in enumerate(data["solutions"][0].keys()):
        # name improvement
        name = improveName(name)
        nameToColumnMap[name] = idx

def readJSONData(filename):
    data      = json.load(open(filename), object_pairs_hook=OrderedDict)
    solutions = data["solutions"]
    table     = np.zeros((len(solutions), len(nameToColumnMap)))

    for i, solution in enumerate(solutions):
        for j, key in enumerate(solution):
            #nameToColumnMap[key] = j
            try:
                val = float(solution[key])
            except TypeError:
                val = 0.0
            table[i, j] = val

    return table


def buildNameToColumnMap(filename):
    if filename.find("json") > 0:
        return buildNameToColumnMapJSON(filename)

    data_format = open(filename, "r").readlines()[0]
    formats = str.split(data_format)

    col_idx = 0
    for col_name in formats:
        if col_name == 'DVAR:' :
            continue
        col_name = improveName(col_name)
        nameToColumnMap[col_name] = col_idx
        col_idx += 1

def readData(filename):

    if filename.find("json") > 0:
        return readJSONData(filename)

    data = np.loadtxt(filename, skiprows=1)

    return data


# Plotting
##############################################################################

def setupPlot(width = 1388.5):

    fig_width_pt  = width
    inches_per_pt = 1.0/72.27                   # Convert pt to inch
    golden_mean   = (math.sqrt(5)-1.0)/2.0      # Aesthetic ratio
    fig_width     = fig_width_pt*inches_per_pt  # width in inches
    fig_height    = fig_width*golden_mean       # height in inches
    fig_size      = [fig_width, fig_height]
    params        = {'backend': 'ps',
                     'axes.labelsize': 14,
                     'font.size': 14,
                     'legend.fontsize': 14,
                     'xtick.labelsize': 14,
                     'ytick.labelsize': 14,
                     'text.usetex': True,
                     'figure.figsize': fig_size}
    pl.rcParams.update(params)


def onpick(event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    print 'onpick points:', zip(xdata[ind], ydata[ind])


def plot(data, xlim, ylim, num, prefix, selected_obj, show_single, plotAll):
    fig = pl.figure()
    ax  = fig.add_subplot(1, 1, 1)

    obj1_idx = nameToColumnMap[selected_obj[0]]
    obj2_idx = nameToColumnMap[selected_obj[1]]
    obj3_idx = nameToColumnMap[selected_obj[2]]
    #obj4_idx = nameToColumnMap[selected_obj[2]]

    vmin = min(data[:, obj3_idx])
    vmax = max(data[:, obj3_idx])

    #x_min = min(data[:, obj1_idx])
    #x_max = max(data[:, obj1_idx])
    #y_min = min(data[:, obj1_idx])
    #y_max = max(data[:, obj1_idx])
    #convert_to_x_axis_scale =  (x_max - x_min) / 1
    #convert_to_y_axis_scale =  (y_max - y_min) / 1
    #max_axis_scale = max(convert_to_x_axis_scale, convert_to_y_axis_scale)

    im  = ax.scatter(data[:, obj1_idx], data[:, obj2_idx],
                     c = data[:, obj3_idx],
                     marker = 's',
                     s = 142,
                     cmap=cm.Spectral, alpha=0.7, vmin=vmin, vmax=vmax)

    # plot the Pareto front by sorting values acc. to x coordinate
    pf_indicies = pl.lexsort(keys = (data[:, obj2_idx], data[:, obj1_idx]))

    x = np.zeros(len(pf_indicies))
    y = np.zeros(len(pf_indicies))

    idx = 0
    for i in pf_indicies:
        x[idx] = data[i, obj1_idx]
        y[idx] = data[i, obj2_idx]
        idx += 1

    ax.plot(x, y, color='orange', linewidth=3, picker=True)


    #FIXME: check that annotate labels do not overlap
    labels = []
    i = 0
    for label in data[:, nameToColumnMap["ID"]]:
        labels.append(str(int(label)))
        i += 1

    for label, x, y in zip(labels, data[:, obj1_idx], data[:, obj2_idx]):
        ax.annotate(label, xy=(x, y), xytext=(25, 25),
                    textcoords='offset points', ha='right', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->',
                    connectionstyle='arc3,rad=0'))

    ax.xaxis.grid(color='gray', linestyle='dashed')
    ax.yaxis.grid(color='gray', linestyle='dashed')

    if show_single:
        af =  AnnoteFinder(data, obj1_idx, obj2_idx,
                           range(len(data[:,obj1_idx])),
                           nameToColumnMap)
        plt.connect('button_press_event', af)

    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])

    plt.xlabel(selected_obj[0])
    plt.ylabel(selected_obj[1])

    ax.yaxis.set_major_formatter(pl.ScalarFormatter(useMathText=True))

    title_text = ('Generation ' + num)
    plt.title(title_text)

    margin = (vmax-vmin)/10
    clow = int(vmin + margin)
    chigh = int(vmax - margin)
    cmiddle = int(vmin + ((vmax-vmin)/2))
    cbar = plt.colorbar(im)
    cbar.set_ticks([clow, cmiddle, chigh])
    cbarlabel_text = selected_obj[2]
    cbar.set_label(cbarlabel_text, labelpad=10)

    if show_single:
        fig.canvas.mpl_connect('pick_event', onpick)
        pl.show()
    else:
        pl.savefig(prefix + '/' + num.zfill(4) + '.png')
        pl.close(fig)

    if show_single and plotAll:
        nrIDs = max(np.shape(data))
        for name,i in nameToColumnMap.iteritems():
            pl.figure()
            pl.hist(data[:,i],bins=nrIDs/10)
            pl.xlabel(name)
            pl.show()


# Helpers
##############################################################################

def saveVideo(img_path, video_name):

    import commands
    # TODO, check if ffmpeg exists - not working
    commands.getoutput("rm " + video_name)
    commands.getoutput("ffmpeg -r 0.7 -i " + img_path +
                       "/%04d.png -b:v 1800 " + video_name)


def computeLimits(data, selected_ids):

    xlim = []
    ylim = []
    xlim.append(1000)
    xlim.append(-1000)
    ylim.append(1000)
    ylim.append(-1000)

    x_idx = nameToColumnMap[selected_ids[0]]
    y_idx = nameToColumnMap[selected_ids[1]]

    for _, d in data.items():
        xlim[1] = max(xlim[1], max(d[:, x_idx]))
        xlim[0] = min(xlim[0], min(d[:, x_idx]))
        ylim[1] = max(ylim[1], max(d[:, y_idx]))
        ylim[0] = min(ylim[0], min(d[:, y_idx]))

    xlim[0] -= 0.05 * (xlim[1] - xlim[0])
    xlim[1] += 0.05 * (xlim[1] - xlim[0])
    ylim[0] -= 0.05 * (ylim[1] - ylim[0])
    ylim[1] += 0.05 * (ylim[1] - ylim[0])

    return (xlim, ylim)


def improveName(name):
    name.lstrip().rstrip()        # remove trailing and leading whitespace
    name = name.lstrip('%')       # remove leading %
    name = name.replace(" ", "")  # remove spaces
    name = name.replace('_','\_') # latex handling of underscore
    name = name.replace('\n', '') # remove newlines
    return name


# Main
##############################################################################

def main(argv):

    selected_ids = []
    path = ""
    videoname = ""
    outpath = "output"
    filename_postfix = "results.json"
    generation = -1
    plotAll = False

    for arg in argv:
        if arg.startswith("--objectives"):
            objectives = str.split(arg, "=")[1]
            for obj in str.split(objectives, ","):
                obj = improveName(obj)
                selected_ids.append(obj)

        elif arg.startswith("--dvars"):
            dvars = str.split(arg, "=")[1]
            for obj in str.split(dvars, ","):
                obj = improveName(obj)
                selected_ids.append(obj)

        elif arg.startswith("--path"):
            path = str.split(arg, "=")[1]

        elif arg.startswith("--filename-postfix"):
            filename_postfix = str.split(arg, "=")[1]

        elif arg.startswith("--outpath"):
            outpath = str.split(arg, "=")[1]

        elif arg.startswith("--video"):
            videoname = str.split(arg, "=")[1]

        elif arg.startswith("--generation"):
            generation = str.split(arg, "=")[1]
        
        elif arg.startswith("--plot-all"):
            plotAll = True
        else:
            print arg,"is not a valid argument"
            return

    if path == "":
        print("ERROR: no path for input data specified")
        return

    if len(selected_ids) != 3:
        print("Please select 3 things to visualize")
        return

    if generation != -1:
        print("Show generation " + generation)


    data = {}
    if generation == -1:
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        buildNameToColumnMap(path + '/' + '2_' + filename_postfix)
        for infile in glob.glob(os.path.join(path + '/',
                                '*_' + filename_postfix)):
            print("Reading data file " + infile)
            num       = str.rsplit(infile, "/", 1)[1]
            num       = str.split (num,    "_", 1)[0]
            data[num] = readData(infile)

        setupPlot()
        (xlim, ylim) = computeLimits(data, selected_ids)
        for i, _ in data.items():
            print " >> saving " + str(i)
            plot(data[str(i)], xlim, ylim,
                 str(i), outpath, selected_ids, show_single=False, plotAll=plotAll)
    else:
        buildNameToColumnMap(path + '/' + str(generation) + '_' +
                             filename_postfix )
        data[str(generation)] = readData(path + '/' + str(generation) + '_' +
                                         filename_postfix)
        setupPlot(867.8)
        (xlim, ylim) = computeLimits(data, selected_ids)
        plot(data[str(generation)], xlim, ylim,
             str(generation), outpath, selected_ids,
             show_single=True, plotAll=plotAll)

    if videoname:
        saveVideo(outpath, videoname)


#call main
if __name__ == "__main__":
    main(sys.argv[1:])

