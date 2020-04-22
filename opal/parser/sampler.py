# Copyright (c) 2018, 2020 Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import json
import os

class SamplerParser:
    """Parses ``*.json`` files of OPAL that are written by the SAMPLE command.

    **Notes**:

    Supports following JSON formats:

    .. code-block:: json

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


    Attributes
    ----------
    __id : str
        (= 'sampler') used to identify the file to be
        a SAMPLE output
    __tag : str
        (= 'name') id tag for file identification
    __begin : int
        Start individual id
    __end : int
        End individual id
    __dvars : list
        The design variables of each individual
    __dvar_bounds : dict
        All design variable bounds
    __objs : list
        The objectives of each individual
    """

    def __init__(self):

        self.__id = 'sampler'
        self.__tag = 'name'

        self.__dvars = []
        self.__dvar_bounds = {}
        self.__objs  = []

        self.__version_tag = 'OPAL version'

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


    def __reset_attributes(self):
        """Clear all private members.
        """
        self.__dvars = []
        self.__dvar_bounds = {}
        self.__objs  = []
        self.__begin = 0
        self.__end   = 0


    def check_file(self, filename):
        """Check if a file is really a sampler output

        Parameters
        ----------
        filename : str
           JSON file to be loaded

        Returns
        -------
        bool
            True if a sampler file, otherwise False
        """
        try:
            self.parse(filename)
            self.__reset_attributes()
        except:
            self.__reset_attributes()
            return False
        return True


    def parse(self, filename):
        """Load the JSON file.

        Parameters
        ----------
        filename : str
            JSON file to be loaded
        """
        if not os.path.exists(filename):
            raise IOError("File '" + filename + "' doesn't exist.")

        try:
            self.__reset_attributes()

            parsed = json.load( open(filename) )

            if not self.__tag in parsed.keys():
                raise IOError("File '" + filename + "' isn't a proper Sample JSON file.")

            if not parsed[self.__tag] == self.__id:
                raise IOError("File '" + filename + "' isn't a proper Sample JSON file.")

            if self.__version_tag in parsed.keys():
                version = parsed[self.__version_tag]

                if version < '2.1.0':
                    raise IOError("Version " + version + " not supported.")

                self.__parse_version_2_1_0(parsed)
            else:
                self.__parse_version_2_0_0(parsed)

            # FIXME Sampler returns a string instead of array for DVAR bounds
            # if it is fixed in the sampler this call can be removed
            self.__fix_bound_type()

        except Exception as e:
            raise e


    def __fix_bound_type(self):
        """Fixes type of DVAR bounds. In the JSON file the bounds are in a string, e.g. '[0, 1]'.

        We need to change to list of floats.
        """
        import re
        for key in self.__dvar_bounds.keys():
            values = self.__dvar_bounds[key]
            if isinstance(values, str):
                obj = re.match('\[(.*), (.*)\]', values)
                if not obj:
                    raise IOError("Error in parsing DVAR bounds.")
                if not len(obj.groups()) == 2:
                    raise IOError("Error in parsing DVAR bounds.")
                self.__dvar_bounds[key] = [float(obj.group(1)), float(obj.group(2))]


    def getIndividual(self, ind):
        """Obtain input values of an individual

        Parameters
        ----------
        ind : int
            Individual number


        Returns
        -------
        dict
            A dictionary with design variable names (keys)
            and their input value.
        """

        if not isinstance(ind, int):
            raise TypeError("Input '" + ind + "' not of type 'int'.")

        if ind < self.__begin or ind > self.__end:
            raise ValueError('No individual with ID > ' + str(ind) + '.')

        return self.__dvars[ind - self.__begin]


    def getObjectives(self, ind):
        """Obtain output values of an individual

        Parameters
        ----------
        ind : int
            Individual number

        Returns
        -------
        dict
            A dictionary with design variable names (keys)
            and their input value.
        """

        if not isinstance(ind, int):
            raise TypeError("Input '" + ind + "' not of type 'int'.")

        if ind < self.__begin or ind > self.__end:
            raise ValueError('No individual with ID > ' + str(ind) + '.')

        return self.__objs[ind]


    @property
    def design_variables(self):
        """Obtain names of design variables.

        Returns
        -------
        list [str]
            A list of strings
        """
        return list( self.bounds.keys() )


    @property
    def bounds(self):
        """Obtain design variable upper and lower bounds

        Returns
        -------
        dict
             A dictionary of design variable names (key) and their bounds
        """
        return self.__dvar_bounds


    @property
    def objectives(self):
        """Obtain names of objectives.

        Returns
        -------
        list [str]
            A list of strings
        """
        if self.__objs:
            return list( self.__objs[0].keys() )
        return []

    @property
    def num_samples(self):
        return self.__end - self.__begin + 1

    @property
    def begin(self):
        """
        Returns
        -------
        int
            Lowest individual ID
        """
        return self.__begin

    @property
    def end(self):
        """
        Returns
        -------
        int
            Highest individual ID
        """
        return self.__end
