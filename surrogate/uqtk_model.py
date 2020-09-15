# Copyright (c) 2019 - 2020, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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

from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted
import os
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class UQTk(BaseEstimator):
    """
    Attributes
    ----------
    _is_fitted : bool
        Have we trained the model?
    fitted_ : numpy.array
        Coefficients of polynomial
    _order : int
        Polynomial order
    _pc_type : str
        Polynomial type
    _pc_basis : str
        Polynomial basis
    _pred_mode : str
        Prediction mode
    _lambda : float
        Regularization parameter
    _pdom : numpy.ndarray
        Domain bounds
    _verbose : bool
        Verbosity
    _method : str
        Training method
    _npar : int
        Number of design variables
    _uqtkbin : str
        'bin' directory of UQTk, i.e, '$UQTK_INS/bin' with 'UQTK_INS' installation directory
    _mindex : numpy.ndarray
        Multiindices of polynomial
    _hasNodes : bool
        Check if nodes and weights for the projection method.
    _nodes : numpy.ndarray
        Nodes for projection method
    _weights : numpy.ndarray
        Weights for projection method
    """

    def __init__(self, pdom, order = 2, **kwargs):
        """
        Parameters
        ----------
        order           PCE order
        """
        self.clear()

        self._uqtkbin= os.path.join(os.environ['UQTK_INS'], "bin")

        if not os.path.exists(os.path.join(self._uqtkbin, 'pce_eval')):
            print ( "You need to set 'UQTK_INS' properly." )
            import sys
            sys.exit()

        self._order   = order
        self._pc_type = 'LU'

        self._method    = kwargs.pop('method', 'lsq')
        self._pc_basis  = kwargs.pop('pc_basis', 'PC_MI')
        self._pred_mode = kwargs.pop('pred_mode','ms')
        self._lambda    = kwargs.pop('regularization', 0.0)
        self._verbose   = kwargs.pop('verbose', False)

        # 2 x n_parameters (1st row: min, 2nd row: max)
        self._pdom = pdom

        if self._method == 'bcs':
            self._tol = kwargs.pop('tol', 1.0e-9)

        self._npar = np.shape(pdom)[1]


    def fit(self, x, y, **kwargs):
        """Train the model.

        Parameters
        ----------
        x  : numpy.ndarray
            Shape NxD with dimension D and number of samples N
        y  : numpy.ndarray
            Shape Nx1
        kwargs : dict, optional
            Further arguments
        """

        ## Generate PC multiindex
        if not self._is_fitted:
            cmd="gen_mi -x'TO' -p"+str(self._order)+" -q"+str(self._npar)+" > gmi.log; mv mindex.dat mi.dat"

            if self._verbose:
                print( "Running "+cmd )
            os.system(os.path.join(self._uqtkbin, cmd))
        else:
            np.savetxt('mi.dat', self._mindex, fmt="%d")

        self._is_fitted = True

        if self._method == 'proj':
            if self._verbose:
                print ("Projection method")
            self._fit_projection(x, y, **kwargs)
        else:
            if self._verbose:
                print ("Regression or BCS: ", self._method)
            self._fit_regression(x, y)

        # get Sobol indices
        self._sobol()

        self._delete_files()

        return self


    def predict(self, x):
        """Predict output.

        Parameters
        ----------
        x : numpy.ndarray
            Input points

        Returns
        -------
        numpy.ndarray
            Predicted output points.
        """
        check_is_fitted(self, '_is_fitted')
        return self._model_pc(x, self.fitted_)


    def main_sensitivity(self):
        """First order Sobol' main sensitivities

        Returns
        -------
        numpy.ndarray
            Main sensitivity indices
        """
        check_is_fitted(self, '_is_fitted')
        return self._allsens_main


    def total_sensitivity(self):
        """Sobol' total sensitivities

        Returns
        -------
        numpy.ndarray
            Total sensitivity indices
        """
        check_is_fitted(self, '_is_fitted')
        return self._allsens_total


    def joint_sensitivity(self):
        """Sobol' joint sensitivities

        Returns
        -------
        numpy.ndarray
            Joint sensitivity indices
        """
        check_is_fitted(self, '_is_fitted')
        return self._allsens_joint


    def evaluate(self, x, pccf):
        """Evaluate polynomial

        Parameters
        ----------
        x : numpy.ndarray
            Input points
        pccf : numpy.array
            Polynomial coefficients
        """
        return self._model_pc(x, pccf)


    def scale(self, x):
        """Scale input points to [-1, 1]
        Parameters
        ----------
        x : numpy.ndarray
            Input points

        Returns
        -------
        numpy.ndarray
            Scaled input points
        """
        LU_transform = MinMaxScaler(feature_range=(-1, 1)).fit(self._pdom)
        return LU_transform.transform(x)

    def _model_pc(self, x, pccf, delete=True):
        """PC surrogate evaluator"""
        np.savetxt('mindex.dat', self._mindex, fmt='%d')
        np.savetxt('pccf.dat', pccf)

        pcbasis = self._pc_basis
        if self._pc_basis == 'PC_MI':
            pcbasis = 'PC_mi'

        # scale [-1, 1]
        x_scaled = self.scale(x)

        np.savetxt('xdata.dat', x_scaled)

        if self._method == 'lsq' or self._method == 'proj':
            cmd = "pce_eval -x'" + pcbasis + "' -o " + str(self._order) \
                + " -f'pccf.dat' -s"+ self._pc_type+" -r'mindex.dat' > fev.log"
        elif self._method == 'bcs' and pcbasis == 'PC_mi':
            cmd="pce_eval -x " + pcbasis + " -f pccf.dat -s " + self._pc_type + " -r mindex.dat > fev.log"
        else:
            print ("Use either 'lsq' or 'bcs' with 'PC_MI'")

        if self._verbose:
            print ( "Running", cmd )
        os.system(os.path.join(self._uqtkbin, cmd))
        pcoutput = np.loadtxt('ydata.dat')

        if delete:
            self._delete_files()

        return pcoutput

    def _fit_regression(self, x, y):
        # scale to [-1, 1]
        x_scaled = self.scale(x)

        np.savetxt('ydata.dat', y)
        np.savetxt('xdata.dat', x_scaled)
        np.savetxt('xcheck.dat',x_scaled)

        if self._method == 'bcs':
            #regression  -m ms -c 1.e-9
            cmd ='regression -l ' + str(self._lambda) + ' -x xdata.dat -y ydata.dat -b '
            cmd += self._pc_basis + ' -s ' + self._pc_type
            cmd += ' -m '+ self._pred_mode + ' -r wbcs -o ' + str(self._order)
            cmd += ' -c ' + str(self._tol)  + ' -p mi.dat > regr.log'
        else: # least squares (lsq)
            cmd ='regression -l ' + str(self._lambda) + ' -x xdata.dat -y ydata.dat -b '
            cmd += self._pc_basis + ' -s '
            cmd += self._pc_type+' -p mi.dat -m '+ self._pred_mode
            cmd += ' -o ' + str(self._order) + ' -r lsq -t xcheck.dat > regr.log'

        if self._verbose:
            print ( "Running "+cmd )
        os.system(os.path.join(self._uqtkbin, cmd))

        # Get the PC coefficients and multiindex
        # fitted == pccf
        self.fitted_ = np.loadtxt('coeff.dat')

        if self._method == 'bcs':
            self._mindex=np.loadtxt('mindex_new.dat',dtype='int')
            np.savetxt('mindex.dat', self._mindex)
        else:
            self._mindex=np.loadtxt('mi.dat',dtype='int')

        ncheck=x_scaled.shape[0]
        ycheck_var=np.zeros((ncheck,))
        sig2=0.0
        self._ccov=np.zeros((self._mindex.shape[0], self._mindex.shape[0]))
        if self._pred_mode != 'm':
            sig2=max(0.0,np.loadtxt('sigma2.dat'))
            self._ccov = np.loadtxt('Sig.dat')
            # This is a cheap hack to tolerate Cholesky error during
            # LSQ when simpler polynomials are given much more complex mindices
            if os.path.isfile('ycheck_var.dat'):
                ycheck_var=np.loadtxt('ycheck_var.dat')
        self.erb=np.sqrt(ycheck_var+sig2)


    def _fit_projection(self, x, y):
        """
        Uses quadrature points to fit that are created by

                generate_quad -d d -g LU -x full -p p+1

            with dimension d and polynomial order p. This yields
            N = (p+1)^d quadrature points and corresponding weights.
        """
        if not self._hasNodes:
            print ("We need the quadrature 'weights'. Call: generate_quadrature()")
            import sys
            sys.exit()

        np.savetxt('qdpts.dat', self._nodes)
        np.savetxt('wghts.dat', self._weights)
        np.savetxt('ydata.dat', y)

        cmd = "pce_resp -x LU -o " + str(self._order) + " -d "
        cmd += str(self._npar) + " -e > pcr.log"

        if self._verbose:
            print ( "Running", cmd )
        os.system(os.path.join(self._uqtkbin, cmd))

        # Get the PC coefficients and multiindex
        self.fitted_ = np.loadtxt('PCcoeff_quad.dat')
        self._mindex = np.loadtxt('mindex.dat',dtype='int')

        ncheck = self._nodes.shape[0]
        ycheck_var = np.zeros((ncheck,))
        self._ccov = np.zeros((self._mindex.shape[0], self._mindex.shape[0]))
        self.erb = np.zeros((ncheck,))


    def _sobol(self):
        # (4c) Compute sensitivities
        np.savetxt('mindex.dat', self._mindex, fmt='%d')
        np.savetxt('PCcoeff.dat', self.fitted_)
        cmd="pce_sens -m'mindex.dat' -f'PCcoeff.dat' -x"+ self._pc_type+" > pcsens.log"
        if self._verbose:
            print ( "Running "+cmd )
        os.system(os.path.join(self._uqtkbin, cmd))
        self._allsens_main = np.loadtxt('mainsens.dat')
        self._allsens_total = np.loadtxt('totsens.dat')
        self._allsens_joint = np.loadtxt('jointsens.dat')
        self._varfrac = np.loadtxt('varfrac.dat')

    def _delete_files(self):
        files = ['coeff.dat',
                 'mainsens.dat',
                 'totsens.dat',
                 'jointsens.dat',
                 'PCcoeff.dat',
                 'ydata.dat',
                 'xdata.dat',
                 'xcheck.dat',
                 'pcsens.log',
                 'gmi.log',
                 'mindex_new.dat',
                 'pccf.dat',
                 'regr.log',
                 'ycheck.dat',
                 'ycheck_var.dat',
                 'varfrac.dat',
                 'sp_mindex.1.dat',
                 'sp_mindex.2.dat',
                 'sp_mindex.3.dat',
                 'selected.dat',
                 'mi.dat',
                 'mindex.dat',
                 'lambdas.dat',
                 'fev.log',
                 'Sig.dat',
                 'sigma2.dat',
                 'errors.dat',
                 'pcr.log',
                 'PCcoeff_quad.dat',
                 'ydata_pc.dat',
                 'gq.log',
                 'qdpts.dat',
                 'wghts.dat']
        for f in files:
            if os.path.exists(f):
                os.remove(f)

    def info(self):
        """Get some information
        """
        return self.fitted_, self._mindex, self._ccov, self._varfrac


    def generate_quadrature(self):
        """Generate nodes and weights for the projection method.

        Returns
        -------
        numpy.ndarray
            Training points generated from quadrature nodes
        """
        self._hasNodes = True

        cmd = 'generate_quad -g LU -d ' + str(self._npar) + ' -p '
        cmd += str(self._order + 1) + ' -x full > gq.log'
        if self._verbose:
            print ( "Running", cmd )
        os.system(os.path.join(self._uqtkbin, cmd))

        self._nodes   = np.loadtxt('qdpts.dat')
        self._weights = np.loadtxt('wghts.dat')

        # 17. March 2020
        # https://stackoverflow.com/questions/21299798/check-if-numpy-array-is-multidimensional-or-not
        if self._nodes.ndim > 1:
            xx = self._unscale(self._nodes[:, 0], self._pdom[:, 0].T)
        else:
            xx = self._unscale(self._nodes, self._pdom[:, 0].T)

        for i in range(1, self._npar):
            xx = np.hstack((xx, self._unscale(self._nodes[:, i], self._pdom[:, i].T)))
        return xx

    def _unscale(self, x, pdom):
        LU_transform = MinMaxScaler(feature_range=(pdom)).fit([[-1], [1]])
        return LU_transform.transform(x.reshape(1, -1)).T


    def clear(self):
        """Reset attributes to initial state.
        """
        self._delete_files()
        self._is_fitted = False
        self.fitted_    = None
        self._mindex    = None
        self._hasNodes  = False
        self._nodes     = None
        self._weights   = None
