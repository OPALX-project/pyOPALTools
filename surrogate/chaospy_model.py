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

import chaospy as cp
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted

class UQChaospy(BaseEstimator):
    """
    Attributes
    ----------
    _hasNodes : bool
        Check if nodes and weights for the projection method.
    _is_fitted : bool
        Have we trained the model?
    fitted_ : numpy.array
        Coefficients of polynomial
    _sens_m : numpy.ndarray
        Main sensitivity indices
    _sens_t : numpy.ndarray
        Total sensitivity indices
    _order : int
        Polynomial order
    _pdom : numpy.ndarray
        Domain bounds
    _verbose : bool
        Verbosity
    _method : str
        Training method
    _npar : int
        Number of design variables
    _distribution : chaospy.distributions.baseclass.Dist
    _kwargs : dict
        Further arguments
    """

    def __init__(self, pdom, order = 2, **kwargs):
        """Constructor.

        Parameters
        ----------
        order : int, optional
            Polynomial expansion order
        pdom : numpy.ndarray
            Domain bounds. numpy.shape(pdom) = 2xN where N is the number of design variables
        verbose : bool, optional
            Verbosity
        method : str, optional
            Training method: 'lsq' (default), 'proj', 'omp', 'lars', 'lasso' or 'elastic_net'.
        kwargs : dict
            Further arguments of a training method.
        """
        self._order = order
        self._pdom = pdom

        self._verbose = kwargs.pop('verbose', False)

        self._method = kwargs.pop('method', 'lsq')

        self._npar = np.shape(pdom)[1]
        self._distribution = cp.Iid(cp.Uniform(-1, 1), self._npar)

        self._kwargs = kwargs.copy()

        if self._verbose:
            print (self._kwargs)

        self.clear()


    def fit(self, x, y):
        """Train the model.

        Parameters
        ----------
        x  : numpy.ndarray
            Shape NxD with dimension D and number of samples N
        y  : numpy.ndarray
            Shape Nx1

        Notes
        -----
        See https://chaospy.readthedocs.io/en/development/tutorial.html
        """
        x = np.asmatrix(x).T
        y = np.asarray(y)
        self._is_fitted = True

        x = np.asarray(self.scale(np.asarray(x).T).T)

        self._pce = cp.orth_ttr(self._order, self._distribution)

        if self._method == 'proj':
            if self._verbose:
                print ("Spectral Projection Method")
            if not self._hasNodes:
                print ("Need 'nodes' and 'weights' as arguments")
                print ( "Call: generate_quadrature()")
                import sys
                sys.exit()
            self.model_ = cp.fit_quadrature(self._pce, self._nodes, self._weights, y)
        elif self._method == 'omp':
            if self._verbose:
                print ("Orthogonal Matching Pursuit")
            # Orthogonal Matching Pursuit (OMP)
            from sklearn.linear_model import OrthogonalMatchingPursuit
            omp = OrthogonalMatchingPursuit(fit_intercept=False, **self._kwargs)
            self.model_ = cp.fit_regression(self._pce, x, y, model=omp)
        elif self._method == 'lars':
            if self._verbose:
                print ("Least Angle Regression")
            from sklearn.linear_model import Lars
            lars = Lars(fit_intercept=False, **self._kwargs)
            self.model_ = cp.fit_regression(self._pce, x, y, model=lars)
        elif self._method == 'lasso':
            if self._verbose:
                print ("Lasso")
            from sklearn.linear_model import Lasso
            lasso = Lasso(fit_intercept=False, **self._kwargs)
            self.model_ = cp.fit_regression(self._pce, x, y, model=lasso)
        elif self._method == 'elastic_net':
            if self._verbose:
                print ("Elastic Net")
            from sklearn.linear_model import ElasticNet
            elastic_net = ElasticNet(fit_intercept=False, **self._kwargs)
            self.model_ = cp.fit_regression(self._pce, x, y, model=elastic_net)
        elif self._method == 'lsq':
            if self._verbose:
                print ("Least Squares Method")
            self.model_ = cp.fit_regression(self._pce, x, y, retall=False)
        else:
            print ("Choose a model: 'proj', 'omp', 'lars', lasso', 'elastic_net' or 'lsq'")
            return self

        self.fitted_ = self.model_.coefficients

        self._sens_m = None
        self._sens_t = None

        return self


    def generate_quadrature(self, rule='G'):
        """Generate nodes and weights for the projection method.

        Parameters
        ----------
        rule : str, optional
            Rule to generate points.

        Returns
        -------
        numpy.ndarray
            Training points generated from quadrature nodes
        """
        self._hasNodes = True

        self._nodes, self._weights = cp.generate_quadrature(self._order,
                                                            self._distribution,
                                                            rule=rule)

        xx = self._unscale(self._nodes[0, :].T, self._pdom[:, 0].T)
        for i in range(1, self._npar):
            xx = np.hstack((xx, self._unscale(self._nodes[i, :].T, self._pdom[:, i])))
        return xx


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
        # x: Nxd
        check_is_fitted(self, '_is_fitted')
        # x: dxN
        x = np.asarray(self.scale(np.asarray(x)).T)
        return self.model_(*x).T

    def main_sensitivity(self):
        """First order Sobol' main sensitivities

        Returns
        -------
        numpy.ndarray
            Main sensitivity indices
        """
        check_is_fitted(self, '_is_fitted')
        if self._sens_m == None:
            try:
                self._sens_m = cp.Sens_m(self.model_, self._distribution)
            except Exception:
                self._sens_m = np.full(self._npar, np.nan)
        return self._sens_m

    def total_sensitivity(self):
        """Sobol' total sensitivities

        Returns
        -------
        numpy.ndarray
            Total sensitivity indices
        """
        check_is_fitted(self, '_is_fitted')
        if self._sens_t == None:
            try:
                self._sens_t = cp.Sens_t(self.model_, self._distribution)
            except Exception:
                self._sens_t = np.full(self._npar, np.nan)
        return self._sens_t

    def mean(self):
        """Expected value operator.

        Returns
        -------
        numpy.ndarray:
            The expected value of the polynomial or distribution
        """
        check_is_fitted(self, '_is_fitted')
        return cp.E(self.model_, self._distribution)

    def std(self):
        """Standard deviation.
        Returns
        -------
        numpy.ndarray:
            Standard deviation
        """
        check_is_fitted(self, '_is_fitted')
        return cp.Std(self.model_, self._distribution)


    def evaluate(self, x, coeffs):
        """Evaluate polynomial

        Parameters
        ----------
        x : numpy.ndarray
            Input points
        coeffs : numpy.array
            Polynomial coefficients
        """
        # x: Nxd

        # x: dxN
        x = np.asarray(self.scale(np.asarray(x)).T)

        # create PCEs
        poly = cp.basis(start=0, stop=self._order, dim=self._npar, sort='G')

        model = cp.dot(poly, coeffs)

        return np.sum(model(*x), axis=0)


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
        x = np.asarray(x, dtype=float)
        lower = np.asarray(self._pdom[0, :], dtype=float)
        upper = np.asarray(self._pdom[1, :], dtype=float)
        return (2.0 * x - (upper + lower)) / (upper - lower)


    def _unscale(self, x, pdom):
        x = np.asarray(x, dtype=float)
        lower, upper = np.asarray(pdom, dtype=float)
        return (((upper - lower) * x.reshape(-1, 1)) + (upper + lower)) / 2.0


    def clear(self):
        """Reset attributes to initial state.
        """
        self._hasNodes  = False
        self._is_fitted = False
        self.fitted_    = None
        self._sens_m    = None
        self._sens_t    = None
