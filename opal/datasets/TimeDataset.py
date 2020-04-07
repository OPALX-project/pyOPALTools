# Author:   Matthias Frey
# Date:     March 2018

from opal.parser.TimingParser import TimingParser
from .DatasetBase import DatasetBase
from opal.visualization.TimingPlotter import TimingPlotter
import os
from opal.utilities.logger import opal_logger

class TimeDataset(DatasetBase, TimingPlotter):
    """
    Attributes
    ----------
    __parser : TimingParser
        Actual data holder
    """
    def __init__(self, directory, fname, ttype='ippl'):
        """Constructor.

        Parameters
        ----------
        directory : str
            Directory of file
        fname : str
            Basename
        ttype : str
            Time file type ('ippl' timing or OPAL 'output')
        """
        try:
            self.__parser = TimingParser()

            if ttype.lower() == 'output':
                self.__parser.read_output_file(os.path.join(directory, fname))
            elif ttype.lower() == 'ippl':
                self.__parser.read_ippl_timing(os.path.join(directory, fname))
            else:
                raise ValueError("Timing file type '" + ttpye + "' not supported." +
                                 "Use either 'ippl' or 'output'")

            super(TimeDataset, self).__init__(directory, fname)
        except Exception as ex:
            opal_logger.exception(ex)


    def getData(self, var, **kwargs):
        """Obtain the timing data

        Parameters
        ----------
        var : str or int
            Timing name or index of timing
        prop : str, optional
            Property, i.e. 'cpu avg', 'cpu max', 'cpu min',
            'wall avg', 'wall max', 'wall min' or
            'cpu tot' and 'wall tot' (only for main timing)

        Returns
        -------
        float
            The timing data
        """
        try:
            dataset = self.__parser.getTiming()

            prop = kwargs.get('prop', '')

            if not prop:
                raise ValueError('You need to specify a property.')

            # find timing dictionary of corresponding property 'prop'
            # 'idx' will be set accordingly
            match = False
            idx = 0
            if isinstance(var, int):
                idx = var
                if idx > -1 and idx < len(dataset):
                    match = True
            else:
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
        except Exception as ex:
            opal_logger.exception(ex)
            return []


    def getLabel(self, var):
        """Obtain label for plotting.

        Parameters
        ----------
        var : str
            String that is returned

        Returns
        -------
        var : str
            Input variable `var`
        """
        return var


    def getLabels(self):
        """
        Obtain all timing names

        Returns
        -------
        list
            Strings with names
        """
        try:
            dataset = self.__parser.getTiming()
            labels = []
            for data in dataset:
                labels.append( data['what'] )
            return labels
        except Exception as ex:
            opal_logger.exception(ex)
            return ''


    def getUnit(self, var):
        """Obtain unit for plotting.

        Parameters
        ----------
        var : str
            Unused

        Returns
        -------
        str
            The string 's' for seconds
        """
        return r'$s$'


    @property
    def size(self):
        return len(self.__parser.getTiming())


    def __str__(self):
        s  = '\n\tTiming dataset.\n\n'
        data = self.__parser.getTiming()
        props = self.__parser.properties
        s += '\tAvailable properties (' + str(len(props)) + ') :\n\n'
        for p in props:
            s += '\t' + p + '\n'
        s += '\n\tAvailable timings (' + str(len(data)) + ') :\n\n'
        for v in data:
            s += '\t' + v['what'] + '\n'
        return s
