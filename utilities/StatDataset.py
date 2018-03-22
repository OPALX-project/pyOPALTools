# Author:   Matthias Frey
# Date:     March 2018

from utilities.SDDSParser import SDDSParser

class StatDataset:
    
    def __init__(self, directory, fname):
        """
        Constructor.
        
        Members
        ----------
        __directory         (str)           of file
        __fname             (str)           name of file
        __parser            (SDDSParser)    actual data holder
        __variable_mapper   (dict)          map user input variable
                                            name to file variable name
        __label_mapper      (dict)          map user input variable
                                            name to plot label name
        """
        self.__directory = directory
        self.__fname = fname
        
        self.__parser = SDDSParser()
        self.__parser.parse(directory + fname)
        
        self.__variable_mapper = {
            'time':     't',
        }
        
        self.__label_mapper  = {
            'rms_x':    r'$\sigma_x$',
            'rms_y':    r'$\sigma_y$',
            'rms_z':    r'$\sigma_z$',
            'rms_px':   r'$\sigma_{px}$',
            'rms_py':   r'$\sigma_{py}$',
            'rms_pz':   r'$\sigma_{pz}$'
        }
    
    
    def getData(self, var, step):
        """
        Obtain data of a variable
        
        Parameters
        ----------
        var     (str)   variable name
        step    (int)   unused
        
        Returns
        -------
        a list of the data
        """
        if var in self.__variable_mapper:
            var = self.__variable_mapper[var]
        return self.__parser.getDataOfVariable(var)
    
    
    def getLabel(self, var):
        """
        Obtain label for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate name plotting ready
        """
        if var in self.__label_mapper:
            var = self.__label_mapper[var]
        return var
    
    
    def getUnit(self, var):
        """
        Obtain unit for plotting.
        
        Parameters
        ----------
        var     (str)   variable name
        
        Returns
        -------
        appropriate unit in math mode for plotting 
        """
        if var in self.__variable_mapper:
            var = self.__variable_mapper[var]
        unit = r'$' + self.__parser.getUnitOfVariable(var) + '$'
        return unit
