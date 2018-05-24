# Author:   Nicole Neveu 
# Date:     May 2018

import numpy as np
import pandas as pd
from opal.datasets.filetype import FileType
from db import mldb

def pareto_pts(x, y):
    """
    Find Pareto points for 2 objectives, given
    all data recorded by optimization run. 
    These points are calculated independent
    of generation. i.e. best points from all 
    generations are found and saved.

    Parameters 
    ----------
    x   (numpy array)   1D array of first objective values
    y   (numpy array)   1D array of second objective values
    
    Optionals
    ---------
    dvars   (numpy array)   ND array of design variables 

    Returns
    -------
    pfdict (dictionary) Dictionary that holds pareto front
                        values and corresponding design values
    """
    #Check data is correct length
    lx = len(x)
    ly = len(y)
    if lx==ly:
        pass
    else: 
        print('Input data sizes do not match\n')
        print('Please check input arrays')
    
    #Making holders for my pareto fronts     
    pts      = []
    pareto_y = []
    pareto_x = []
    pfdict   = {}
    w  = np.arange(0,1.001, 0.001)
    sx = scaleData(x)
    sy = scaleData(y)
    
    #Finding locations of best points 
    #with respect to all weights (w)
    for i in range(0, len(w)):
        fobj    = sy * w[i] + sx *(1-w[i])
        wmins   = np.where(fobj==min(fobj))[0][0]
        pts     = np.append(pts, wmins)

    ind = (np.unique(pts)).astype(int)
    pareto_x = x[ind]
    pareto_y = y[ind]

    #Reordering values for easier plotting
    #Maybe not the best way to do this?
    reorder = sorted(zip(*[pareto_x, pareto_y, ind]))     
    pfdict['x'], pfdict['y'], ind = list(zip(*reorder))

    #Return array(ind) so it can be used as index
    #in dictinary arrays
    return(pfdict, np.array(ind))
    #return(pareto_pts.ix[:,0], pareto_pts.ix[:,1], pdvar) #pareto_x, pareto_y, pdvar)


def get_all_data_db(dbpath):
    """
    Get all objectives and design variables
    from every generation in an optimzation
    or ml database. Databases are made using 
    OPAL output from json files or stat files. 
    Functions to make databases can be found
    in mldb.py. 
    
    Parameters 
    ----------
    db  (str)   path to pickle file containing 
                database made with mldb.py

    Returns
    -------
    data    (dict)  Dictonary containing all 
                    objectives and design values
                    in optimization database.
    """
    data = {}
    dbr = mldb.mldb()
    dbr.load(dbpath)
    dvar_names = dbr.getXNames()
    obj_names  = dbr.getYNames()
    num_gens   = dbr.getNumberOfSamples()
  
    #Make arrays with data from all generations
    for gen in range(0, num_gens):
        dvals   = dbr.getAllDvar(gen)
        objvals = dbr.getAllObj(gen)
        if gen==0:
            alldvals = dvals
            allobjs  = objvals
        else:
            alldvals = np.append(alldvals, dvals, axis=0)
            allobjs  = np.append(allobjs, objvals, axis=0)

    #Make dict entries for design variables 
    for i,dname in enumerate(dvar_names):
        data[dname] = alldvals[:,i]

    #Make dict entries for objectives
    for j,objname in enumerate(obj_names):
        data[objname] = allobjs[:,j]
    
    return(data)


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


def delete_repeats(x, y, z=0):
    """
    Delete repeated pareto front values, if any.
    
    Parameters
    ----------
    x   (numpy array)   1D array of first objective values
    y   (numpy array)   1D array of second objective values
   
    Optionals
    ---------
    z   (numpy array)   ND array of second design variables

    Returns
    -------
    df  (pandas db) database with out repeats
    """
    if z==0:
        df = pd.DataFrame({'x':x, 'y':y}) #, 'z':z})
    else:
        df = pd.DataFrame({'x':x, 'y':y, 'z':z})
    
    return df.drop_duplicates(subset=['x', 'y'], keep='first')

