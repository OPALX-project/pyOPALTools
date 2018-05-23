# Author:   Nicole Neveu 
# Date:     May 2018


import numpy as np
import pandas as pd
from opal.datasets.filetype import FileType
from db import mldb

def pareto(x, y, dvars=0):
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
    ld = len(dvars[:,0])
    if lx==ly==ld:
        pass
    else: 
        print('Input data sizes do not match\n')
        print('Please check input arrays')
    
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

    #Check dvars is correct length
    if dvars!=0:
        pdvar      = dvars[ind, :]

    return(pareto_pts.ix[:,0], pareto_pts.ix[:,1], pdvar) #pareto_x, pareto_y, pdvar)


def get_all_data_db(dbpath):
    """
    Get all objectives and design variables
    from every generation in an optimzation
    database. Databases are made using OPAL 
    output from json files or stat files. 
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
    #dvars  = dbr.getXNames()
    #obj    = dbr.getYNames()
    gens   = dbr.getNumberOfSamples()

    
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

    """
    if z==0:
        df = pd.DataFrame({'x':x, 'y':y}) #, 'z':z})
    else:
        df = pd.DataFrame({'x':x, 'y':y, 'z':z})
    
    return df.drop_duplicates(subset=['x', 'y'], keep='first')

