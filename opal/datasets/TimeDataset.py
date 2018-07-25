# Author:   Matthias Frey
# Date:     March 2018

from timing.Timing import Timing
from opal.datasets.DatasetBase import *
import os

class TimeDataset(DatasetBase):
    
    def __init__(self, directory, fname, ttype='ippl'):
        """
        Constructor.
        
        Parameters
        ----------
        directory   (str)   of file
        fname       (str)   basename
        ttype       (str)   time file type ('ippl' timing or OPAL 'output')
        
        Members
        -------
        __parser            (Timing)    actual data holder
        """
        self.__parser = Timing()
        
        if ttype.lower() == 'output':
            self.__parser.read_output_file(os.path.join(directory, fname))
        elif ttype.lower() == 'ippl':
            self.__parser.read_ippl_timing(os.path.join(directory, fname))
        else:
            raise ValueError("Timing file type '" + ttpye + "' not supported." +
                             "Use either 'ippl' or 'output'")
        
        super(TimeDataset, self).__init__(directory, fname)
    
    
    def getData(self, var, **kwargs):
        """
        Obtain the timing data
        
        Parameters
        ----------
        var     (str/int)   timing name or index of timing
        prop    (str)       property, i.e. 'cpu avg', 'cpu max', 'cpu min',
                            'wall avg', 'wall max', 'wall min' or
                            'cpu tot' and 'wall tot' (only for main timing)
        
        Returns
        -------
        the timing data
        """
        dataset = self.__parser.getTiming()
        
        prop = kwargs.get('prop', '')
        
        if not prop:
            raise ValueError('You need to specify a property.')
        
        # find timing dictionary of corresponding property 'prop'
        # 'idx' will be set accordingly
        idx = 0
        if isinstance(var, int):
            idx = var
            if idx > -1 and idx < len(dataset):
                match = True
        else:
            match = False
            available = []
            for data in dataset:
                if var == data['what']:
                    match = True
                    break
                else:
                    available.append( data['what'] )
                    idx += 1
    
        if not match:
            raise ValueError("No timing called '" + var + "'. Possible entries:"
                             + str(available))
        
        if not prop in dataset[idx]:
            raise ValueError("Timing '" + var + "' has not property '"
                             + prop + "'")
        
        return dataset[idx][prop]
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   is returned
        
        Returns
        -------
        var
        """
        return var
    
    
    def getLabels(self):
        """
        Obtain all timing names
        
        Parameters
        ----------
        None
        
        Returns
        -------
        a list of strings with names
        """
        dataset = self.__parser.getTiming()
        labels = []
        for data in dataset:
            labels.append( data['what'] )
        return labels
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   unused
        
        Returns
        -------
        the string 's' for seconds
        """
        return r'$s$'
