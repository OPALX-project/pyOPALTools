# Copyright (c) 2018, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

import os
from opal.datasets.filetype import FileType
from opal.utilities.logger import opal_logger

class DatasetBase:
    """Class with member functions common to all datasets.

    Attributes
    ----------
    _directory : str
        Directory of file
    _fname : str
        Name of file
    _ftype : FileType
        Type of file
    """

    def __init__(self, directory, fname):
        """Constructor.
        """
        try:
            full_path = os.path.join(directory, fname)
            if not os.path.exists(full_path):
                raise RuntimeError("File '" + full_path + "' does not exist.")

            self._directory = directory
            self._fname = fname
            self._ftype = FileType.extensionToFileType(os.path.join(directory, fname))
        except Exception as ex:
            opal_logger.exception(ex)


    @property
    def filetype(self):
        return self._ftype


    @property
    def filename(self):
        return os.path.join(self._directory, self._fname)


    def getData(self, var, **kwargs):
        """
        To be implemented by derived class.
        """
        pass


    def getUnit(self, var):
        """
        To be implemented by derived class.
        """
        pass


    def getLabel(self, var):
        """
        To be implemented by derived class.
        """
        pass

    def getLabelWithUnit(self, var):
        """
        Returns
        -------
        str
            plotting label with unit
        """
        return self.getLabel(var) + ' [' + self.getUnit(var) + ']'

    @property
    def size(self):
        """
        To be implemented by derived class.
        """
        return None

    def __str__(self):
        """
        Print a short summary about the dataset.
        To be implemented in the derived classes.
        """
        return 'Empty dataset.'


    @property
    def ds(self):
        """
        Returns
        -------
        reference to dataset. Used in plotting classes.
        """
        return self
