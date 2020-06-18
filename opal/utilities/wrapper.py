# Copyright (c) 2020, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Wrapper functions.
# We wrap functions according to
# https://stackoverflow.com/questions/35758323/hook-python-module-function
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import matplotlib.pyplot as plt
import matplotlib as mpl
import functools
import inspect
import re

def wrapper(fun, new_fun):
    """Wrapper.

    Parameters
    ----------
    fun : function
        the function to wrap
    new_fun : function
        the new function that is called before
        calling the original function
    """
    @functools.wraps(fun)
    def run(*args, **kwargs):
        return new_fun(fun, *args, **kwargs)
    return run


def new_label(fun, *args, **kwargs):
    """New function for matplotlib text.

    Parameters
    ----------
    fun : function
        the original label matplotlib function
    args : tuple
        arguments of the original function
    kwargs : dict
        further keyword arguments of the original function
    """
    fun_args = inspect.getargspec(fun)

    idx = -1
    if 'label' in fun_args.args:
        idx = fun_args.args.index('label')
    elif 's' in fun_args.args:
        idx = fun_args.args.index('s')

    if idx == -1:
        return fun(*args, **kwargs)

    if mpl.rcParams['text.usetex']:
        signs = frozenset('$[](){}\\-') # symbols not to escape due to LaTex
        lst = list(args)
        if isinstance(lst[idx], str):
            # we need to add the signs otherwise LaTex formulas
            # are not properly compiled
            re._alphanum_str = re._alphanum_str.union(signs)
            lst[idx] = re.escape(lst[idx])
            # remove signs again
            re._alphanum_str = re._alphanum_str.difference(signs)
            args = tuple(lst)
    return fun(*args, **kwargs)



mpl.axis.Axis.set_label_text = wrapper(mpl.axis.Axis.set_label_text, new_label)

mpl.axes.Axes.set_title = wrapper(mpl.axes.Axes.set_title, new_label)

mpl.axes.Axes.text = wrapper(mpl.axes.Axes.text, new_label)
