# Author:   Matthias Frey
# Date:     23. May 2018

import json
import os

class SamplerParser:
    """
    Parses *.json files of OPAL that are written by the SAMPLE command.
    
    Notes
    -----
    Expects following JSON format:
    {
        "name": "sampler",
        "dvar-bounds": {
            "MX": "[ 16, 32 ]",
            "nstep": "[ 10, 40 ]"
        },
        "samples": [
            {
                "ID": "0",
                "dvar": {
                    "MX": "20",
                    "nstep": "33"
                }
            },
            {
                "ID": "1",
                "dvar": {
                    "MX": "21",
                    "nstep": "29"
                }
            }
        ]
    }
    
    Members
    -------
    __id (= 'sampler')  (str)   used to identify the file to be
                                a SAMPLE output
    __tag (= 'name')    (str)   id tag for file identification
    __keys              (list)  all allowed JSON keys
                                (check property SamplerParser.keys)
    __parsed            (dict)  loaded file
    """
    
    def __init__(self):
        
        self.__id = 'sampler'
        self.__tag = 'name'
        
        self.__keys = [
            'dvar-bounds',
            'samples'
        ]
        
        self.__parsed = None
    
    
    def parse(self, filename):
        """
        Load the JSON file.
        
        Parameters
        ----------
        filename    (str)   JSON file to be loaded
        
        Returns
        -------
        None
        """
        if not os.path.exists(filename):
            raise IOError("File '" + filename + "' doesn't exist.")
        
        try:
            self.__parsed = json.load( open(filename) )
            
            if not self.__tag in self.__parsed.keys():
                raise # call IOError at end
            
            if not self.__parsed[self.__tag] == self.__id:
                raise # call IOError at end
            
            for key in self.__keys:
                if not key in self.__parsed.keys():
                    raise # call IOError at end
        except:
            raise IOError("File '" + filename + "' isn't a proper Sample JSON file.")
    
    
    def getValue(self, key):
        """
        Obtain either bounds or all samples
        (i.e. all individual input values).
        
        Parameter
        --------
        key     (str)   of SAMPLE JSON
        
        
        Returns
        -------
        data
        """
        if not key in self.__parsed.keys():
            raise KeyError("Key '" + key + "' not in SAMPLE JSON file.")
        return self.__parsed[key]
    
    
    def getIndividual(self, ind):
        """
        Obtain input values of an individual
        
        Parameter
        ---------
        ind     (int)   individual number
        
        Returns
        -------
        a dictionary with design variable names (keys)
        and their input value.
        """
        
        if not isinstance(ind, int):
            raise TypeError("Input '" + ind + "' not of type 'int'.")
        
        if ind < 0:
            raise ValueError('No individual with ID < 0.')
        
        samples = self.__parsed['samples']
        
        n = len(samples - 1)
        
        if ind > n:
            raise ValueError('No individual with ID > ' + str(n) + '.')
        
        if int(samples[ind]['ID']) == ind:
            # fast access (if ordered)
            return samples[ind]['dvar']
        else:
            # slow access
            for i, sample in enumerate(samples):
                if int(sample['ID']) == ind:
                    return sample['dvar']
            raise ValueError('Individual with ID ' + str(ind) + ' not found.')
    
    
    @property
    def keys(self):
        """
        Obtain all available keys.
        
        Returns
        -------
        list of strings
        """
        return self.__keys
    
    
    @property
    def design_variables(self):
        """
        Obtain names of design variables.
        
        Returns
        -------
        a list of strings
        """
        return list( self.bounds.keys() )
    
    
    @property
    def bounds(self):
        """
        Obtain design variable upper and lower bounds
        
        Returns
        -------
        a dictionary of design variable names (key) and their bounds
        """
        return self.__parsed['dvar-bounds']
