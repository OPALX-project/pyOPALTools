from scipy.interpolate import Rbf
import numpy as np

class Interpolator:
    """ It is built on scipy.interpolate.Rbf
        It has to be used with python3.x
    """
    
    ##
    def __init__(self):
        """
        Parameters
        ----------
        
        """
        self.__rbfi = []
    
    ##
    def train(self, coords, values, function='linear', smooth=0):
        """ Train the interpolator with values at
            given coordinates coords
        
        Parameters
        ----------
        coords  : coordinates of the nodes (each column is an axis)
        values  : values of the nodes
        
        Returns
        -------
        None
        
        Notes
        -----
        For further information about scipy.interpolate.Rbf see
        https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.interpolate.Rbf.html
        """
        
        # 21. June 2017
        # https://stackoverflow.com/questions/27046533/unpack-numpy-array-by-column
        # https://stackoverflow.com/questions/12720450/unpacking-arguments-only-named-arguments-may-follow-expression
        self.__rbfi = Rbf(*coords.T, values, function=function, smooth=smooth)
    
    
    ##
    def evaluate(self, coords):
        """ Interpolate to new coordinates coords
        
        Parameters
        ----------
        coords  : new coordinates where to interpolate
        
        Returns
        -------
        interpolated values
        
        Notes
        -----
        None
        """
        return self.__rbfi(*coords)