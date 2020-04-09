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

class H5Error(Exception):
    """Base class for H5 exceptions.
    (see also https://docs.python.org/2/tutorial/errors.html)

    Attributes
    ----------
    __msg : str
        explanation of the error
    """
    pass

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return '\033[91m\033[1mError: ' + self.__msg + '\033[0m'


class H5ParseError(H5Error):
    """Exception raised for errors in parsing.
    """
    def __init__(self, msg):
        super(H5ParseError, self).__init__(msg)


class H5OverflowError(H5Error):
    """Exception raised for errors in accessing data.
    """
    def __init__(self, msg):
        super(H5OverflowError, self).__init__(msg)


class H5AttributeError(H5Error):
    """Exception raised for errors concerning attributes.
    """
    def __init__(self, msg):
        super(H5AttributeError, self).__init__(msg)


class H5DatasetError(H5Error):
    """Exception raised for errors concerning datasets.
    """
    def __init__(self, msg):
        super(H5DatasetError, self).__init__(msg)
