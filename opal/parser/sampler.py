# Author:   Matthias Frey
# Date:     23. May 2018

import json
import os

class SamplerParser:
    """
    Parses *.json files of OPAL that are written by the SAMPLE command.
    
    Notes
    -----
    Supports following JSON formats:
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
    
    {
        "samples": {
            "0": {
                "dvar": {
                    "MX": "16",
                    "nstep": "10"
                },
                "obj": {
                    "o1": 22.2,
                    "o2": 22.1
                }
            },
            "1": {
                "dvar": {
                    "MX": "19",
                    "nstep": "11"
                },
                "obj": {
                    "o1": 21.2,
                    "o2": 23.1
                }
            },
            "2": {
                "dvar": {
                    "MX": "22",
                    "nstep": "12"
                },
                "obj": {
                    "o1": 12.2,
                    "o2": 32.1
                }
            }
        },
        "name": "sampler",
        "OPAL version": "2.0.0",
        "git revision": "1849b7e5130657e8be50d524de0f6c50134f330a",
        "dvar-bounds": {
            "MX": "[ 16, 32 ]",
            "nstep": "[ 10, 40 ]"
        }
    }
    
    
    Members
    -------
    __id (= 'sampler')  (str)   used to identify the file to be
                                a SAMPLE output
    __tag (= 'name')    (str)   id tag for file identification
    __begin             (int)   start individual id
    __end               (int)   end individual id
    __dvars             ([])    the design variables of each
                                individual
    __dvar_bounds       ({})    all design variable bounds
    __objs              ([])    the objectives of each individual
    """
    
    def __init__(self):
        
        self.__id = 'sampler'
        self.__tag = 'name'
        
        self.__dvars = []
        self.__dvar_bounds = {}
        self.__objs  = []
        
        self.__version_tag = 'OPAL version'
        self.__version_support = {
            '2.1.0': self.__parse_version_2_1_0
        }
    
    def __parse_version_2_0_0(self, data):
        samples = data['samples']
        nSamples = len(samples)
        
        self.__dvar_bounds = data['dvar-bounds']
        
        self.__begin = 0
        self.__end   = 0
        
        for ind in range(0, nSamples):
            # make sure it's sorted
            real_id = int(samples[ind]['ID'])
            
            self.__begin = min(real_id, self.__begin)
            self.__end   = max(real_id, self.__end)
            
            self.__dvars.insert(real_id, samples[ind]['dvar'])
    
    
    def __parse_version_2_1_0(self, data):
        samples = data['samples']
        
        self.__dvar_bounds = data['dvar-bounds']
        
        self.__begin = min(list(map(int, samples.keys())))
        self.__end   = max(list(map(int, samples.keys())))
        
        for ind in range(self.__begin, self.__end+1):
            self.__dvars.append(samples[str(ind)]['dvar'])
            
            if 'obj' in samples[str(ind)].keys() and samples[str(ind)]['obj']:
                self.__objs.append(samples[str(ind)]['obj'])
    
    
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
            parsed = json.load( open(filename) )
            
            if not self.__tag in parsed.keys():
                raise IOError("File '" + filename + "' isn't a proper Sample JSON file.")
            
            if not parsed[self.__tag] == self.__id:
                raise IOError("File '" + filename + "' isn't a proper Sample JSON file.")
            
            if self.__version_tag in parsed.keys():
                version = parsed[self.__version_tag]
                
                if not version in self.__version_support.keys():
                    raise IOError("Version " + version + " not supported.")
                
                self.__version_support[version](parsed)
            else:
                self.__parse_version_2_0_0(parsed)
            
        except Exception as e:
            raise e
    
    
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
        
        if ind < self.__begin or ind > self.__end:
            raise ValueError('No individual with ID > ' + str(ind) + '.')
        
        return self.__dvars[ind]
    
    
    def getObjectives(self, ind):
        """
        Obtain output values of an individual

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

        if ind < self.__begin or ind > self.__end:
            raise ValueError('No individual with ID > ' + str(ind) + '.')

        return self.__objs[ind]


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
        return self.__dvar_bounds


    @property
    def objectives(self):
        """
        Obtain names of objectives.

        Returns
        -------
        a list of strings
        """
        if self.__objs:
            return list( self.__objs[0].keys() )
        return []

    @property
    def num_samples(self):
        return self.__end - self.__begin + 1
