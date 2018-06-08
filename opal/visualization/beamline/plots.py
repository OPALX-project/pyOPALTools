# Author:    Ryan Roussel
# Date:      June 2018

import matplotlib.pyplot as plt

from opal.datasets.ElementDataset import ElementDataset
from .. import helper

def plot_beamline_elements(ds,**kwargs):
     """
     Plot a 2D projection (z-x) of the beamline elements
    
     Parameters
     ----------
     ds      (DatasetBase)       dataset
    
     Optional parameters
     -------------------
     ax      (matplotlib.axes.Axes)     axes object for plotting
     fill    (boolean)                  fill with color?
        
     Returns
     -------
     a matplotlib.axes.Axes object
     """
     
     if not isinstance(ds, ElementDataset):
          raise TypeError("Dataset '" + ds.filename + "' not derived from 'ElementDataset'.")
     ax = helper.get_axes(kwargs.pop('axes',''))

     fill = kwargs.pop('fill',False)


     for ele in ds.getOutlines():
          if fill:
               ax.fill(*ele.T,alpha=0.5)
          else:
               ax.plot(*ele.T)

     return ax

