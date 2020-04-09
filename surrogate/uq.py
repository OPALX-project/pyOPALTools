# Copyright (c) 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
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
from surrogate.bootstrap import Bootstrap

class UQ(BaseEstimator):

    def __init__(self, order = 2):
        """
        Parameters
        ----------
        order : int, optional
            PCE order
        """
        self._order = order


    def fit(self, x, y):
        """
        Parameters
        ----------
        x : array_like (N,D,)
            Shape NxD with dimension D and number of samples N
        y : array_like (N,Q,)
            Shape NxQ with quantities of interest Q and number of samples N

        Notes
        -----
        See https://chaospy.readthedocs.io/en/development/tutorial.html
        """
        self._x = np.asmatrix(x)
        self._y = np.asarray(y)
        self._is_fitted = True

        # figure out the range
        dists = []
        for i in range(np.shape(x)[1]):
            dists.append( cp.Uniform(np.min(x[:, i]),
                                     np.max(x[:, i])) )

        self._distribution = cp.J(*dists)

        self._pce = cp.orth_ttr(self._order, self._distribution)

        self.model_ = cp.fit_regression(polynomials=self._pce,          # Polynomial expansion with
                                                                        # polynomials.shape=(M,) and polynomials.dim=D
                                        abscissas=np.transpose(x),      # Collocation nodes with abscissas.shape=(D,K)
                                        evals=y,                        # Model evaluations with len(evals)=K
                                        rule='LS',
                                        retall=False,                   # If True return Fourier coefficients in addition to R
                                        order=0,                        # Tikhonov regularization order
                                        alpha=None)

        self.fitted_ = self.model_.coefficients

        return self


    def predict(self, x):
        check_is_fitted(self, '_is_fitted')
        x = np.asarray(x).T
        return self.model_(*x)

    def main_sensitivity(self):
        check_is_fitted(self, '_is_fitted')
        return cp.Sens_m(self.model_, self._distribution)

    def total_sensitivity(self):
        check_is_fitted(self, '_is_fitted')
        return cp.Sens_t(self.model_, self._distribution)

    def mean(self):
        check_is_fitted(self, '_is_fitted')
        return cp.E(self.model_, self._distribution)

    def std(self):
        check_is_fitted(self, '_is_fitted')
        return cp.Std(self.model_, self._distribution)


    def confidence_interval(self, x, y, alpha, **kwargs):
        """Compute confidence intervals using the bootstrap method

        Parameters
        ----------
        x : array_like (N,D,)
            Shape NxD with dimension D and number of samples N
        y  : array_like (N,)
            Shape Nx1 with quantities of interest Q and number of samples N
        alpha : float
            CI

        Returns
        -------
        numpy.ndarray
            Sorted y_train
        numpy.ndarray
            y_pred
        numpy.ndarray
            Lower bound for CI
        numpy.ndarray
            Upper bound for CI
        """
        bs = Bootstrap(self)
        bs.boot(x, y, **kwargs)

        y_pred = self.predict(x)

        # create PCEs
        dim = np.shape(x)[1]
        poly = cp.basis(start=0, stop=self._order, dim=dim, sort='G')

        lo, up = bs.confidence_interval(alpha=alpha)
        lo_pce = cp.inner(poly, np.asarray(lo))
        up_pce = cp.inner(poly, np.asarray(up))

        # evaluate predicte lower and upper bounds
        x = np.asarray(x).T
        y_lo = lo_pce(*x)
        y_up = up_pce(*x)

        # in order to plot we need to sort
        permute = np.argsort(y)
        y_pred  = y_pred[permute]
        y       = y[permute]
        y_lo    = y_lo[permute]
        y_up    = y_up[permute]
        return y, y_pred, y_lo, y_up
