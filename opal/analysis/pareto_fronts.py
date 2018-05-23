# Author:   Nicole Neveu 
# Date:     May 2018

from opal.datasets.filetype import FileType
from opal.statistics import statistics as stat
from opal.datasets.DatasetBase import DatasetBase
from opal.analysis import impl_beam
import numpy as np

import json
import pylab as pl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

from collections import OrderedDict
from optPilot.Annotate import AnnoteFinder
import pyOPALTools.optPilot.OptPilotJsonReader as jsonreader


def scaleData(vals):
    """
    Scale 1D data array from 0 to 1.
    Used to compare objectives with different units.

    Parameters
    ----------
    vals    (numpy array)   1D array that holds any opal data

    Returns
    -------
    sacaled_vals    (numpy array)   1D array scaled from 0 to 1
    """
    smax = np.max(vals)
    smin = np.min(vals)
    scaled_vals = (vals - smin)/smax
    return (scaled_vals)

def pareto(x, y, dvars=0):
    """
    Find Pareto points for 2 objectives given
    all data recorded by optimization run. 
    These points are calculated independent
    of generation. i.e. best points from all 
    generations are found and saved.

    Parameters 
    ----------
    x   (numpy array)   array of first objective values
    y   (numpy array)   array of second objective values
    
    Optionals
    ---------
    dvars
    """
    #Making holders for my pareto fronts            
    pareto_y = []
    pareto_x = []
    pdvar    = []
    w  = np.arange(0,1.001, 0.001)
    sx = scaleData(x)
    sy = scaleData(y)
    #Finding best point with respect to all weights (w)
    for i in range(0, len(w)):
        fobj     = sy * w[i] + sx *(1-w[i])
        wmins    = np.where(fobj==min(fobj))[0][0]
        pareto_y = np.append(pareto_y, y[wmins])
        pareto_x = np.append(pareto_x, x[wmins])

    pareto_pts = delete_repeats(pareto_x, pareto_y)
    ind        = np.array(pareto_pts.index.tolist())
    pdvar      = dvars[ind, :]

    return(pareto_pts.ix[:,0], pareto_pts.ix[:,1], pdvar) #pareto_x, pareto_y, pdvar)

def delete_repeats(x, y): #, z):
    df = pd.DataFrame({'x':x, 'y':y}) #, 'z':z})
    return df.drop_duplicates(subset=['x', 'y'], keep='first')

