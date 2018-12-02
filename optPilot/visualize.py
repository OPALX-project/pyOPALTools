#!/usr/bin/python
import os
import sys
import glob
import json
import math

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from collections import OrderedDict

from optPilot.Annotate import AnnoteFinder

import opal.parser.OptimizerParser import OptimizerParser as jsonreader

# Data parsing
##############################################################################

# name of the columns in the solution data
nameToColumnMap = {}
selected_ids = []
path = ""
videoname = ""
outpath = "./"
filename_postfix = "results.json"
generation = -1
plotAll = False
    
data = { } 

def readJSONData(filename):
    dirname = os.path.dirname(filename)
    optjson = jsonreader(dirname + '/')
    
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


def improveName(name):
    name.lstrip().rstrip()        # remove trailing and leading whitespace
    name = name.lstrip('%')       # remove leading %
    name = name.replace(" ", "")  # remove spaces
    name = name.replace('_','\_') # latex handling of underscore
    name = name.replace('\n', '') # remove newlines
    return name


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

def getXY(generation,path,filename_postfix,selected_ids):        

    fn = path + '/' + str(generation) + '_' + filename_postfix

    data[str(generation)] = readJSONData(fn)

    (xlim, ylim) = computeLimits(data, selected_ids)

    obj1_idx = nameToColumnMap[selected_ids[0]]
    obj2_idx = nameToColumnMap[selected_ids[1]]
    
    x = data[str(generation)][:, obj1_idx]
    y = data[str(generation)][:, obj2_idx]

    return x,y

class Plotter:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def setupPlot(self,width = 1388.5):
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

    def plot(self, obj):
        self.obj = obj
        # self.obj.readData()
        self.l = plt.plot(obj.getX(),obj.getY(),'*')
        _vars = obj.get_variables()
        plt.subplots_adjust(bottom=0.03*(len(_vars)+2))
        self.sliders = []
        self.buttons = [] 

        for i,var in enumerate(_vars):
            self.add_slider(i*0.03, var[0], var[1], var[2])

        self.add_reset()    
        plt.show()

    def add_reset(self):
        axcolor = 'lightgoldenrodyellow'
        ax = plt.axes([0.9, 0.9, 0.1, 0.04])
        resbutt  = Button(ax, 'Reset', color=axcolor, hovercolor='0.975')
        self.buttons.append(resbutt)
        def update(val):
            self.obj.readInitialData()
            self.l[0].set_ydata(self.obj.getY())
            self.l[0].set_xdata(self.obj.getX())
            self.sliders[0].reset()
            self.fig.canvas.draw_idle()
        resbutt.on_clicked(update)

    def add_slider(self, pos, name, min, max):
        ax = plt.axes([0.1, 0.02+pos, 0.8, 0.02], axisbg='lightgoldenrodyellow')
        slider = Slider(ax, name, min, max, valinit=int(self.obj.generation), valfmt="%d") 
        self.sliders.append(slider)
        def update(val):
            self.obj.readData()
            setattr(self.obj, name, val)
            self.l[0].set_ydata(self.obj.getY())
            self.l[0].set_xdata(self.obj.getX())
            self.fig.canvas.draw_idle()
        slider.on_changed(update)

class OptData:

    def __init__(self,generation,path,filename_postfix,selected_ids):
        self.generation=generation
        self.initialgeneration=generation
        self.path=path
        self.filename_postfix=filename_postfix
        self.selected_ids=selected_ids
        self.x,self.y = getXY(generation,path,filename_postfix,selected_ids)
    
    def readData(self):
        self.x,self.y = getXY(int(self.generation),self.path,self.filename_postfix,self.selected_ids)

    def readInitialData(self):
        self.x,self.y = getXY(int(self.initialgeneration),self.path,self.filename_postfix,self.selected_ids)
     
    def getX(self):
        return self.x

    def getY(self):
        return self.y
        
    def get_variables(self):
        return [
            ('generation', 0., 5000.)
        ]


def main(argv):

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

    k = Plotter()
    k.setupPlot()
    k.plot(OptData(generation,path,filename_postfix,selected_ids))

#call main
if __name__ == "__main__":    main(sys.argv[1:])
