import chaospy as cp
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_is_fitted
from bootstrap import Bootstrap

class UQ(BaseEstimator):

    def __init__(self, order = 2):
        self._order = order


    def fit(self, X, y):
        """
        X       shape NxD with dimension D and number of samples N
        y       shape NxQ with quantities of interest Q and number of samples N

        Notes
        -----
        See https://chaospy.readthedocs.io/en/development/tutorial.html
        """
        self._X = np.asmatrix(X)
        self._y = np.asarray(y)
        self._is_fitted = True

        # figure out the range
        dists = []
        for i in range(np.shape(X)[1]):
            dists.append( cp.Uniform(np.min(X[:, i]),
                                     np.max(X[:, i])) )

        self._distribution = cp.J(*dists)

        self._pce = cp.orth_ttr(self._order, self._distribution)

        self.model_ = cp.fit_regression(polynomials=self._pce,          # Polynomial expansion with
                                                                        # polynomials.shape=(M,) and polynomials.dim=D
                                        abscissas=np.transpose(X),      # Collocation nodes with abscissas.shape=(D,K)
                                        evals=y,                        # Model evaluations with len(evals)=K
                                        rule='LS',
                                        retall=False,                   # If True return Fourier coefficients in addition to R
                                        order=0,                        # Tikhonov regularization order
                                        alpha=None)

        self.fitted_ = self.model_.coefficients

        return self


    def predict(self, X):
        check_is_fitted(self, '_is_fitted')
        X = np.asarray(X).T
        return self.model_(*X)

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
        bs = Bootstrap(self)
        bs.boot(x, y, **kwargs)

        y_pred = self.predict(x)

        # create PCEs
        dim = np.shape(x)[1]
        poly = cp.basis(start=0, stop=self._order, dim=dim, sort='G')

        lo, up = bs.confidence_interval(alpha=alpha)
        lo_pce = cp.dot(poly, np.asarray(lo))
        up_pce = cp.dot(poly, np.asarray(up))

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



    #def get_params(self, deep=True):
        ## suppose this estimator has parameters "alpha" and "recursive"
        #return {"order": self._order}

    #def set_params(self, **parameters):
        #for parameter, value in parameters.items():
            #setattr(self, parameter, value)
        #return self
