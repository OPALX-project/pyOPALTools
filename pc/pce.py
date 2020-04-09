# Copyright (c) 2018, Andreas Adelmann, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-

import os, sys
#sys.path.insert(0, '/Users/adelmann/git/')
#sys.path.insert(0, '/Users/adelmann/git/pyOPALTools/')

if sys.version_info[0] < 3:
  # Python 2
  import cPickle as pick
else:
  # Python 3
  import pickle as pick

import numpy as np

def getPCData(fn):
    if (os.path.isfile(fn)):
        with open(fn, 'rb') as pickle_file:
            if sys.version_info.major > 2:
                u = pick.load(pickle_file,encoding='latin1')
            else:
                u = pick.load(pickle_file)
    else:
        print ('Training points not found, run analysis first')
        sys.exit()
    return u

class pceEval:

    def __init__(self,fn,verbose=True):

        self.pctype='LEG_N'
        self.u                   = getPCData(fn)
        self.data                = self.u[0]
        self.pcc                 = self.data['pcmi'][0]
        self.mi                  = self.data['pcmi'][1]
        self.order               = self.data['order']
        self.dim                 = len(self.pcc)
        self.modelParameterDom   = self.data['training'][0]
        #
        if not verbose:
            print('pceEval initialized')
            print ("Data file              ", fn)
            print ("Order                  ", self.order)# look at the random sample first
            print ("modelParameterDom      ",self.modelParameterDom )
            for i in range(self.dim):
                print ("QoI                    ", self.u[i]['training'][5])


    def evalPc(self,x,d):
        """Use external pce_eval (should be written in Py)
        """
        xscaled = (2.0 * x-(self.modelParameterDom[:,1]+self.modelParameterDom[:,0])) / (self.modelParameterDom[:,1]-self.modelParameterDom[:,0])
        np.savetxt('/tmp/mindex.dat',self.mi[d],fmt='%d')
        np.savetxt('/tmp/pccf.dat',self.pcc[d])
        np.savetxt('/tmp/xdata.dat', xscaled.reshape(1, xscaled.shape[0]))
        cmd="pushd . && cd /tmp && $UQTK_SRC/src_cpp/bin/pce_eval -x'PC_mi' -f'pccf.dat' -s"+self.pctype+" -r'mindex.dat' > fev.log && popd"
        os.system(cmd)
        pcoutput=np.loadtxt('/tmp/ydata.dat')
        return pcoutput
