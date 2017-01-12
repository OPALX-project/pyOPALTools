#!/usr/bin/env python
#
#
import mmap
import pandas as pd
import numpy as np
import re
import sys
import glob
import h5py

from math import cos, sin, fmod

import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec

from matplotlib.pyplot import *
from matplotlib import rc

import scipy
from scipy import stats

if sys.version_info < (3, 0):
    import commands as subprocess
else:
    import subprocess

from scipy.stats import kurtosis


def set_colors(npar):
    """ Sets a list of different colors of requested length"""
    colors = []
    pp=1+npar/6
    for i in range(npar):
        c=1-(float) (i/6)/pp
        b=np.empty((3))
        for jj in range(3):
            b[jj]=c*int(i%3==jj)
        a=int(i%6)/3
        colors.append(((1-a)*b[2]+a*(c-b[2]),(1-a)*b[1]+a*(c-b[1]),(1-a)*b[0]+a*(c-b[0])))
    
    return colors

#                                                                                                                                                                  
# All about plotting                                                                                                                                               
#                                                                                                                                                                  

rc('xtick.major', pad=10)
rc('savefig', dpi=800)
rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman'], 'weight': 100, 'size': 16})
rc('ytick', labelsize=16)
rc('xtick', labelsize=16)
rc('savefig', dpi=800)

global tableau20

def tickLabel(ax):
        ticklabels_x = ax.get_xticklabels()
        for label in ticklabels_x:
          label.set_fontsize(12)
          label.set_family('serif')
        ticklabels_y = ax.get_yticklabels()
        for label in ticklabels_y:
          label.set_fontsize(12)
          label.set_family('serif')

enu = ['a) ','b) ', 'c)' ]

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
                  (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]



"""
A very crude reader for H5hut data

"""
class H5Reader:

    def __init__(self, filename):
        self.__filename = filename
        self.__hf = h5py.File(self.__filename,'r')
        if self.__hf:
            print ("Open sucsessfully ",filename)
        else:
            print ("Give up on ",filename)
            sys.exit()
                
    def getStepData(self, step, attrName):
        x = []
        dataStr = 'Step#'+str(step)+"/"+attrName
        x = self.__hf.get(dataStr)
        return x[:]

    def printH5Info(self):
        print('List of arrays in this file: ', self.__hf.keys())
        data = self.__hf.get('Step#0')
        np_data = np.array(data)
        print('Shape of the array Step#0: ', np_data.shape)

    def getH5Steps(self):
        return len(self.__hf.keys())







"""
A very crude parser for SDDS files (produced by OPAL simulation runs).

The parser does not check if the SDDS file is valid. Result files can be
large, therefore we map the file to memory preventing reading everything. The
user can get values at fixed dump steps (get()) or at specific positions [m]
with getAtSpos.
"""

class SddsReader:

    def __init__(self, filename):
        self.columns = {}
        self.columnNames = []
        self.params = {}
        self.data_pos = []
        self.sdds_data_mem = 0
        self.data_start = 0
        
        self.memoryMapFile(filename)
        self.parseHeader()


    def __del__(self):
        self.sdds_data_mem.close()


    def get(self, name, position = -2):
        self.sdds_data_mem.seek(self.data_pos[position])

        line = self.sdds_data_mem.readline().decode("utf-8")
        column_idx = self.columns[name]
        return float(line.split("\t")[column_idx])


    def getColumn(self, name):
        column = []
        for i in range(0, len(self.data_pos) - 1):
            column.append(self.get(name, i))
        return column

    def getAttributes(self):
        attrs = []
        attrs.append(" ".join(self.columnNames))
        return attrs

    def findClosestDumps(self, name, position_m):
        spos_before  = 0
        value_before = 0
        spos_after   = 0
        value_after  = 0

        for i in range(0, len(self.columns) - 1):
            cursor_pos = self.get('s', i)

            if position_m < cursor_pos:
                index_before = max(0, i-1)
                value_before = self.get(name, index_before)
                value_after  = self.get(name, i)
                spos_before  = self.get('s', index_before)
                spos_after   = cursor_pos
                return ( (spos_before, value_before),
                         (spos_after, value_after) )

        raise LookupError("Specified position (" + position_m + ") never \
                           reached by simulation")


    def getAtSpos(self, name, position_m):
        (before, after) = self.findClosestDumps(name, position_m)

        # simple linear interpolation
        interpolated_value = 0.0
        interpolated_value = before[1]
        if position_m - before[0] > 1e-8:
            interpolated_value += (position_m - before[1]) * \
                    (after[1] - before[1]) / (after[0] - before[0])

        return interpolated_value


    def memoryMapFile(self, filename):
        try:
            f = open(filename, "r+")
        except IOError:
            print('Cannot open SDDS file ' + filename)
        else:
            self.sdds_data_mem = mmap.mmap(f.fileno(), 0)


    def parseHeader(self):

        column_idx = 0
        param_idx = 0

        # file starts with 'SDDS1'
        line = self.sdds_data_mem.readline()
        line = self.sdds_data_mem.readline()
        while(line):

            line = line.decode("utf-8")

            if line.startswith("&description"):
                # strange linebreak in sdds description
                line = self.sdds_data_mem.readline()

            elif line.startswith("&parameter"):
                param_name = line.split(",")[0]
                param_name = param_name.split("name=")[1]
                self.params[param_name] = param_idx
                param_idx += 1

            elif line.startswith("&column"):
                column_name = line.split(",")[0]
                column_name = column_name.split("name=")[1]
                self.columnNames.append(column_name)
                self.columns[column_name] = column_idx
                column_idx += 1

            elif line.startswith("&data"):
                self.sdds_data_mem.readline()
                self.sdds_data_mem.readline()
                self.data_start = self.sdds_data_mem.tell()
                break

            else:
                raise Exception("Invalid syntax in SDDS header")

            line = self.sdds_data_mem.readline()

        self.data_pos.append(self.sdds_data_mem.tell())
        line = self.sdds_data_mem.readline()
        while(line):
            self.data_pos.append(self.sdds_data_mem.tell())
            line = self.sdds_data_mem.readline()


