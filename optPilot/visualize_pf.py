#!/usr/bin/python
# Copyright (c) 2010 - 2013, Yves Ineichen, ETH Zürich
#                      2017, Jochem Snuverink, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Toward massively parallel multi-objective optimization with application to
# particle accelerators" (https://doi.org/10.3929/ethz-a-009792359)
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import glob
import json
import math
import argparse

import numpy as np
import pylab as pl

import matplotlib.cm     as cm
import matplotlib.pyplot as plt
from collections import OrderedDict

from optPilot.Annotate import AnnoteFinder

from opal.parser.OptimizerParser import OptimizerParser as jsonreader


# Data parsing
##############################################################################

# name of the columns in the solution data
nameToColumnMap = {}

def readJSONData(filename):
    dirname = os.path.dirname(filename)
    optjson = jsonreader()
    optjson.parse(dirname + '/')

    # get the generation from the filename
    basename = os.path.basename(filename)
    generation = int( str.split(basename, "_", 1)[0] )
    optjson.readGeneration(generation)

    #
    # make plain format
    #

    # build name to column map
    dvars = optjson.getDesignVariables()
    objs  = optjson.getObjectives()
    idname   = "ID"

    idx = 0
    for name in dvars:
        nameToColumnMap[name] = idx
        idx += 1

    for name in objs:
        nameToColumnMap[name] = idx
        idx += 1

    nameToColumnMap[idname] = idx

    # build data matrix by stacking columns [dvars objsval ids]
    dvarval = optjson.getAllInput()
    objsval = optjson.getAllOutput()
    ids     = optjson.getIDs()

    data = np.column_stack((dvarval, objsval, ids))

    return data


def readDAT_0(filename):
    data_format = open(filename, "r").readlines()[0]
    formats = str.split(data_format)

    col_idx = 0
    for col_name in formats:
        if col_name == 'DVAR:' :
            continue
        col_name = improveName(col_name)
        nameToColumnMap[col_name] = col_idx
        col_idx += 1

    data = np.loadtxt(filename, skiprows=1)

    return data


def readData(filename):

    if filename.find("json") > 0:
        return readJSONData(filename)

    return readDAT_0(filename)


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
    print ('onpick points:', zip(xdata[ind], ydata[ind]))


def plot(data, xlim, ylim, num, prefix, selected_obj, show_single, plotAll):
    fig = pl.figure()
    ax  = fig.add_subplot(1, 1, 1)

    obj1_idx = nameToColumnMap[selected_obj[0]]
    obj2_idx = nameToColumnMap[selected_obj[1]]
    obj3_idx = nameToColumnMap[selected_obj[2]]

    vmin = min(data[:, obj3_idx])
    vmax = max(data[:, obj3_idx])

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
        pl.savefig(prefix + '/pf.png')
    else:
        pl.savefig(prefix + '/' + num.zfill(4) + '.png')
        pl.close(fig)

    if show_single and plotAll:
        nrIDs = max(np.shape(data))
        for name,i in nameToColumnMap.items():
            pl.figure()
            pl.hist(data[:,i],bins=int(nrIDs/10))
            pl.xlabel(name)
            pl.show()

# Helpers
##############################################################################

def saveVideo(img_path, video_name):
    import subprocess
    import distutils
    from distutils import spawn
    video_name = video_name + ".mp4"
    if distutils.spawn.find_executable("ffmpeg") != None:
        output = subprocess.getoutput("ffmpeg -y -framerate 0.7 -i " + img_path + "/%04d.png " +
                                    "-qscale 0 -r 0.7 " + video_name)
    else:
        print ('Video exporting is not possible, ffmpeg is not installed.')

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
    outpath = "./"
    filename_postfix = "results.json"
    generation = -1
    plotAll = False

    try:
        ## Parse input arguments
        parser = argparse.ArgumentParser()

        parser.add_argument("-o",
                            "--objectives",
                            dest="objectives",
                            type=str,
                            default='',
                            help="specify 3 objectives you want to visualize (check header of "
                            "result file for available objectives), e.g. --objectives=%OBJ1,%OBJ2,%OBJ3")

        parser.add_argument("-d",
                            "--dvars",
                            dest="dvars",
                            type=str,
                            default='',
                            help="Design variables")

        parser.add_argument("-p",
                            "--path",
                            dest="path",
                            type=str,
                            default=path,
                            help="specify the path of the result files")

        parser.add_argument("-f",
                            "--filename-postfix",
                            dest="filename_postfix",
                            type=str,
                            default=filename_postfix,
                            help="(default: 'results.json'): specify a custom file postfix of result files")

        parser.add_argument("-u",
                            "--outpath",
                            dest="outpath",
                            type=str,
                            default=outpath,
                            help="path for storing resulting pngs")

        parser.add_argument("-a",
                            "--plotall",
                            dest="plotall",
                            type=bool,
                            default=plotAll,
                            help="display additional histogram distributions for the design variables "
                            "and objectives (for a specific generation only)")

        parser.add_argument("-g",
                            "--generation",
                            dest="generation",
                            type=int,
                            default=generation,
                            help="only displays the 'n'-th generation")

        parser.add_argument("-v",
                            "--video",
                            dest="video",
                            type=str,
                            default=videoname,
                            help="(untested): name of the video")

        args = parser.parse_args()


        if args.objectives:
            for obj in str.split(args.objectives, ","):
                obj = improveName(obj)
                selected_ids.append(obj)

        if args.dvars:
            for obj in str.split(args.dvars, ","):
                obj = improveName(obj)
                selected_ids.append(obj)

        path             = args.path
        filename_postfix = args.filename_postfix
        outpath          = args.outpath
        videoname        = args.video
        generation       = args.generation
        plotAll          = args.plotall

        if path == "":
            raise SyntaxError('No path for input data specified')

        if len(selected_ids) != 3:
            raise SyntaxError('Please select exactly 3 things to visualize')
            return

        if generation != -1:
            print("Show generation " + generation)

        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        data = {}
        if generation == -1:
            for infile in glob.glob(os.path.join(path,
                                    '*_' + filename_postfix)):
                print("Reading data file " + infile)
                num       = str.rsplit(infile, "/", 1)[1]
                num       = str.split (num,    "_", 1)[0]
                data[num] = readData(infile)

            setupPlot()
            (xlim, ylim) = computeLimits(data, selected_ids)
            for i, _ in data.items():
                print (" >> saving " + str(i))
                plot(data[str(i)], xlim, ylim,
                    str(i), outpath, selected_ids, show_single=False, plotAll=plotAll)
        else:
            data[str(generation)] = readData(path + '/' + str(generation) + '_' +
                                            filename_postfix)
            setupPlot(867.8)
            (xlim, ylim) = computeLimits(data, selected_ids)
            plot(data[str(generation)], xlim, ylim,
                str(generation), outpath, selected_ids,
                show_single=True, plotAll=plotAll)

        #if videoname:
        saveVideo(outpath, videoname)

    except:
        print ( '\n\t\033[01;31mError: ' + str(sys.exc_info()[1]) + '\n' )


#call main
if __name__ == "__main__":
    main(sys.argv[1:])
