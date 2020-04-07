# Author: Matthias Frey
# Date:   March 2018
# According: https://docs.python.org/2/tutorial/errors.html

class H5Error(Exception):
    """Base class for H5 exceptions.

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
