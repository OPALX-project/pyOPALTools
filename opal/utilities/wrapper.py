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

def my_escape(pattern):
    _alphanum_str = frozenset(
    "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890$")
    _alphanum_bytes = frozenset(
        b"_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890$")
    """
    Escape all the characters in pattern except ASCII letters, numbers and '_'.
    """
    if isinstance(pattern, str):
        alphanum = _alphanum_str
        s = list(pattern)
        for i, c in enumerate(pattern):
            if c not in alphanum:
                if c == "\000":
                    s[i] = "\\000"
                else:
                    s[i] = "\\" + c
        return "".join(s)
    else:
        alphanum = _alphanum_bytes
        s = []
        esc = ord(b"\\")
        for c in pattern:
            if c in alphanum:
                s.append(c)
            else:
                if c == 0:
                    s.extend(b"\\000")
                else:
                    s.append(esc)
                    s.append(c)
        return bytes(s)


def wrapper(fun, new_fun):
    @functools.wraps(fun)
    def run(*args, **kwargs):
        return new_fun(fun, *args, **kwargs)
    return run


def new_label(fun, *args, **kwargs):
    fun_args = inspect.getargspec(fun)

    idx = -1
    if 'label' in fun_args.args:
        idx = fun_args.args.index('label')
    elif 's' in fun_args.args:
        idx = fun_args.args.index('s')

    if idx == -1:
        return fun(*args, **kwargs)

    if mpl.rcParams['text.usetex']:
        lst = list(args)
        if isinstance(lst[idx], str):
            lst[idx] = my_escape(lst[idx])
            args = tuple(lst)
    return fun(*args, **kwargs)





mpl.axis.Axis.set_label_text = wrapper(mpl.axis.Axis.set_label_text, new_label)

mpl.axes.Axes.set_title = wrapper(mpl.axes.Axes.set_title, new_label)

mpl.axes.Axes.text = wrapper(mpl.axes.Axes.text, new_label)


#def wrapper(fun, new_fun):
    #"""Wrapper.

    #Parameters
    #----------
    #fun : function
        #the function to wrap
    #new_fun : function
        #the new function that is called before
        #calling the original function
    #"""
    #@functools.wraps(fun)
    #def run(*args, **kwargs):
        #return new_fun(fun, *args, **kwargs)
    #return run


#def new_plt_label(fun, s, *args, **kwargs):
    #"""New function for matplotlib axis labels.

    #Parameters
    #----------
    #fun : function
        #the original label matplotlib function
    #s : str
        #the label
    #args : tuple
        #further arguments to the original label function
    #kwargs : dict
        #further keyword arguments to the original label function
    #"""
    #isTex = mpl.rcParams['text.usetex']
    #if isTex:
        #s = re.escape(s)
    #return fun(s, *args, **kwargs)

#def new_plt_text(fun, x, y, s, fontdict=None, **kwargs):
    #"""New function for matplotlib axis labels.

    #Parameters
    #----------
    #fun : function
        #the original label matplotlib function
    #s : str
        #the label
    #args : tuple
        #further arguments to the original label function
    #kwargs : dict
        #further keyword arguments to the original label function
    #"""
    #isTex = mpl.rcParams['text.usetex']
    #if isTex:
        #s = re.escape(s)
    #return fun(x, y, s, fontdict, **kwargs)


## wrap matplotlib.pyplot.xlabel
#plt.xlabel = wrapper(plt.xlabel, new_plt_label)

## wrap matplotlib.pyplot.xlabel
#plt.ylabel = wrapper(plt.ylabel, new_plt_label)

## wrap matplotlib.pyplot.text
#plt.text = wrapper(plt.text, new_plt_text)
