# Author:   Ryan Roussel
# Date:     May 2018

import matplotlib

def get_axes(ax):
    """
    Return an ax object if it exists or create a figure and
    return that axes
    Parameters
    ----------
    ax     (test object)    test object 
    """
    
    if not isinstance(ax,matplotlib.axes.Axes):
        fig, ax = matplotlib.pyplot.subplots()
    return ax
    
